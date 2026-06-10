from django.conf import settings
from django.db import models

from notes.models import Note


class Summary(models.Model):
    SUMMARY_TYPES = [
        ('bullet', 'Bullet Summary'),
        ('paragraph', 'Paragraph Summary'),
        ('exam', 'Exam-Focused Summary'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='summaries')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='summaries')
    summary_type = models.CharField(max_length=20, choices=SUMMARY_TYPES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.note.title} - {self.get_summary_type_display()}'

# Create your models here.
