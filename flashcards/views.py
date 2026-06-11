import csv

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from notes.models import Note
from .forms import FlashcardGenerateForm
from .models import Flashcard, FlashcardProgress
from .services import generate_flashcards


@login_required
def flashcard_list(request):
    cards = Flashcard.objects.filter(user=request.user).select_related('note')
    notes_with_cards = Note.objects.filter(user=request.user, flashcards__isnull=False).distinct()
    progress_totals = FlashcardProgress.objects.filter(user=request.user).aggregate(
        reviews=Sum('review_count'),
        known=Sum('known_count'),
    )
    return render(
        request,
        'flashcards/list.html',
        {
            'cards': cards,
            'notes_with_cards': notes_with_cards,
            'review_count': progress_totals['reviews'] or 0,
            'known_count': progress_totals['known'] or 0,
        },
    )


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


@login_required
def revise_flashcards(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    cards = list(Flashcard.objects.filter(user=request.user, note=note).order_by('pk'))
    position = max(int(request.GET.get('position', 0)), 0)

    if not cards:
        return render(request, 'flashcards/revise.html', {'note': note, 'complete': True, 'total': 0})

    if position >= len(cards):
        progress = FlashcardProgress.objects.filter(user=request.user, flashcard__note=note)
        totals = progress.aggregate(reviews=Sum('review_count'), known=Sum('known_count'))
        reviews = totals['reviews'] or 0
        known = totals['known'] or 0
        mastery = round((known / reviews) * 100) if reviews else 0
        return render(
            request,
            'flashcards/revise.html',
            {
                'note': note,
                'complete': True,
                'total': len(cards),
                'mastery': mastery,
            },
        )

    card = cards[position]
    if request.method == 'POST':
        result = request.POST.get('result')
        if result in {'known', 'again'}:
            progress, _ = FlashcardProgress.objects.get_or_create(user=request.user, flashcard=card)
            progress.review_count += 1
            if result == 'known':
                progress.known_count += 1
            progress.save()
        return redirect(f"{request.path}?position={position + 1}")

    return render(
        request,
        'flashcards/revise.html',
        {
            'note': note,
            'card': card,
            'position': position,
            'display_position': position + 1,
            'total': len(cards),
            'complete': False,
        },
    )
