from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from xhtml2pdf import pisa

from .forms import QuizGenerateForm
from .models import Quiz
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
    return render(request, 'quiz/detail.html', {'quiz': quiz})


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
