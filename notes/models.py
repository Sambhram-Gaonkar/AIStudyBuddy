from django.conf import settings
from django.db import models


class Subject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_subject_name_per_user'),
        ]

    def __str__(self):
        return self.name


class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes')
    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        related_name='notes',
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='notes/')
    extracted_text = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title


class NoteChunk(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='chunks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='note_chunks')
    text = models.TextField()
    page_number = models.PositiveIntegerField(null=True, blank=True)
    chunk_index = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['note_id', 'chunk_index']
        unique_together = ['note', 'chunk_index']

    def __str__(self):
        return f'{self.note.title} chunk {self.chunk_index}'

# Create your models here.
