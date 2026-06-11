from django.conf import settings
from django.db import models

from notes.models import Note


class Flashcard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='flashcards')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='flashcards')
    front = models.CharField(max_length=255)
    back = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['front']

    def __str__(self):
        return self.front


class FlashcardProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='flashcard_progress')
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE, related_name='progress')
    review_count = models.PositiveIntegerField(default=0)
    known_count = models.PositiveIntegerField(default=0)
    last_reviewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'flashcard'], name='unique_flashcard_progress'),
        ]

    @property
    def mastery_percentage(self):
        if not self.review_count:
            return 0
        return round((self.known_count / self.review_count) * 100)

    def __str__(self):
        return f'{self.flashcard.front}: {self.mastery_percentage}%'
