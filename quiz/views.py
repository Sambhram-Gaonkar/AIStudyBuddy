from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from xhtml2pdf import pisa

from .forms import QuizGenerateForm
from .models import Quiz, QuizAttempt
from .services import generate_quiz


@login_required
def quiz_list(request):
    quizzes = Quiz.objects.filter(user=request.user)
    return render(request, 'quiz/list.html', {'quizzes': quizzes})


@login_required
def generate_quiz_view(request):
    if request.method == 'POST':
        form = QuizGenerateForm(request.POST, user=request.user)
        if form.is_valid():
            quiz = generate_quiz(
                user=request.user,
                note=form.cleaned_data['note'],
                question_type=form.cleaned_data['question_type'],
                difficulty=form.cleaned_data['difficulty'],
                number_of_questions=form.cleaned_data['number_of_questions'],
            )
            return redirect('quiz:detail', pk=quiz.pk)
    else:
        form = QuizGenerateForm(user=request.user)

    return render(request, 'quiz/generate.html', {'form': form})


@login_required
def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk, user=request.user)
    attempts = quiz.attempts.filter(user=request.user)[:5]
    return render(request, 'quiz/detail.html', {'quiz': quiz, 'attempts': attempts})


def normalize_answer(value):
    return ' '.join(value.lower().strip().split())


def is_correct_answer(question, submitted_answer):
    normalized_submitted = normalize_answer(submitted_answer)
    normalized_correct = normalize_answer(question.correct_answer)
    if normalized_submitted == normalized_correct:
        return True

    if len(normalized_correct) == 1 and normalized_correct in 'abcd':
        option_index = ord(normalized_correct) - ord('a')
        if option_index < len(question.options):
            return normalized_submitted == normalize_answer(question.options[option_index])
    return False


@login_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk, user=request.user)
    questions = list(quiz.questions.all())

    if request.method == 'POST':
        answers = {}
        score = 0
        for question in questions:
            answer = request.POST.get(f'question_{question.pk}', '').strip()
            answers[str(question.pk)] = answer
            if is_correct_answer(question, answer):
                score += 1

        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            answers=answers,
            score=score,
            total_questions=len(questions),
        )
        return redirect('quiz:attempt_result', pk=attempt.pk)

    return render(request, 'quiz/take.html', {'quiz': quiz, 'questions': questions})


@login_required
def attempt_result(request, pk):
    attempt = get_object_or_404(
        QuizAttempt.objects.select_related('quiz'),
        pk=pk,
        user=request.user,
        quiz__user=request.user,
    )
    question_results = []
    for question in attempt.quiz.questions.all():
        submitted_answer = attempt.answers.get(str(question.pk), '')
        question_results.append({
            'question': question,
            'submitted_answer': submitted_answer,
            'is_correct': is_correct_answer(question, submitted_answer),
        })
    return render(
        request,
        'quiz/attempt_result.html',
        {'attempt': attempt, 'question_results': question_results},
    )


@login_required
def export_quiz_pdf(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk, user=request.user)
    template = get_template('quiz/pdf.html')
    html = template.render({'quiz': quiz})
    output = BytesIO()
    result = pisa.CreatePDF(html, dest=output)
    if result.err:
        return HttpResponse('Could not generate PDF.', status=500)
    response = HttpResponse(output.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=\"quiz-{quiz.pk}.pdf\"'
    return response
