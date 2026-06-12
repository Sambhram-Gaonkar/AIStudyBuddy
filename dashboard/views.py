from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import render

from quiz.models import QuizAttempt


@login_required
def home(request):
    notes = request.user.notes.all()
    attempts = QuizAttempt.objects.filter(user=request.user).select_related('quiz', 'quiz__note')
    attempt_count = attempts.count()
    average_score = round(
        sum(attempt.percentage for attempt in attempts) / attempt_count
    ) if attempt_count else 0
    topic_performance = list(
        attempts.values('quiz__note__title')
        .annotate(average=Avg('score'), average_total=Avg('total_questions'))
        .order_by('average')
    )
    for topic in topic_performance:
        total = topic['average_total'] or 0
        topic['percentage'] = round((topic['average'] / total) * 100) if total else 0

    context = {
        'total_notes': notes.count(),
        'recent_notes': notes[:5],
        'total_quizzes': request.user.quizzes.count(),
        'recent_quizzes': request.user.quizzes.select_related('note')[:5],
        'total_flashcards': request.user.flashcards.count(),
        'recent_flashcards': request.user.flashcards.select_related('note')[:5],
        'total_summaries': request.user.summaries.count(),
        'recent_summaries': request.user.summaries.select_related('note')[:5],
        'attempt_count': attempt_count,
        'average_score': average_score,
        'recent_attempts': attempts[:5],
        'topic_performance': topic_performance[:6],
        'weak_topics': [topic for topic in topic_performance if topic['percentage'] < 60][:3],
    }
    return render(request, 'dashboard/home.html', context)

# Create your views here.
