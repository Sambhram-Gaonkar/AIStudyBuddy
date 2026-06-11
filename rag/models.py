from django.conf import settings
from django.db import models

from notes.models import Note


class ChatHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_history')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='chat_history')
    question = models.TextField()
    answer = models.TextField()
    source_chunks = models.JSONField(default=list, blank=True)
    retrieval_mode = models.CharField(max_length=30, blank=True)
    used_llm = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.question[:80]
