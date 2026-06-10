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

# Create your models here.
