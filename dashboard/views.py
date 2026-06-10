from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    notes = request.user.notes.all()
    context = {
        'total_notes': notes.count(),
        'recent_notes': notes[:5],
        'total_quizzes': request.user.quizzes.count(),
        'recent_quizzes': request.user.quizzes.select_related('note')[:5],
        'total_flashcards': request.user.flashcards.count(),
        'recent_flashcards': request.user.flashcards.select_related('note')[:5],
        'total_summaries': request.user.summaries.count(),
        'recent_summaries': request.user.summaries.select_related('note')[:5],
    }
    return render(request, 'dashboard/home.html', context)

# Create your views here.
