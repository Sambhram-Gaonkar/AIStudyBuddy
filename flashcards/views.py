import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from notes.models import Note
from .forms import FlashcardGenerateForm
from .models import Flashcard
from .services import generate_flashcards


@login_required
def flashcard_list(request):
    cards = Flashcard.objects.filter(user=request.user).select_related('note')
    notes_with_cards = Note.objects.filter(user=request.user, flashcards__isnull=False).distinct()
    return render(request, 'flashcards/list.html', {'cards': cards, 'notes_with_cards': notes_with_cards})


@login_required
def generate_flashcards_view(request):
    if request.method == 'POST':
        form = FlashcardGenerateForm(request.POST, user=request.user)
        if form.is_valid():
            generate_flashcards(
                user=request.user,
                note=form.cleaned_data['note'],
                number_of_cards=form.cleaned_data['number_of_cards'],
            )
            return redirect('flashcards:list')
    else:
        form = FlashcardGenerateForm(user=request.user)

    return render(request, 'flashcards/generate.html', {'form': form})


@login_required
def export_flashcards_csv(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    cards = Flashcard.objects.filter(user=request.user, note=note)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=\"flashcards-{note.pk}.csv\"'
    writer = csv.writer(response)
    writer.writerow(['Term', 'Definition'])
    for card in cards:
        writer.writerow([card.front, card.back])
    return response
