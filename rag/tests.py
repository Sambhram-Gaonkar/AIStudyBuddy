from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

from .models import ChatHistory


class ChatHistoryTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username='student', password='password123')
        self.other_user = user_model.objects.create_user(username='other', password='password123')
        self.note = Note.objects.create(
            user=self.user,
            title='Biology',
            file=SimpleUploadedFile('biology.pdf', b'%PDF-1.4'),
            extracted_text='Cells are the basic unit of life.',
        )
        self.client.force_login(self.user)

    @patch('rag.views.answer_question')
    def test_question_and_answer_are_saved(self, mock_answer_question):
        mock_answer_question.return_value = {
            'answer': 'Cells are the basic unit of life.',
            'sources': [{
                'note_title': 'Biology',
                'page_number': 2,
                'chunk_index': 1,
            }],
            'retrieval_mode': 'keyword',
            'used_llm': False,
        }

        response = self.client.post(reverse('rag:chat'), {
            'note': self.note.id,
            'question': 'What is a cell?',
        })

        self.assertEqual(response.status_code, 200)
        history = ChatHistory.objects.get(user=self.user)
        self.assertEqual(history.note, self.note)
        self.assertEqual(history.question, 'What is a cell?')
        self.assertEqual(history.source_chunks[0]['page_number'], 2)
        self.assertContains(response, 'What is a cell?')

    def test_page_only_shows_current_users_history(self):
        ChatHistory.objects.create(
            user=self.user,
            note=self.note,
            question='Visible question',
            answer='Visible answer',
        )
        other_note = Note.objects.create(
            user=self.other_user,
            title='Private note',
            file=SimpleUploadedFile('private.pdf', b'%PDF-1.4'),
        )
        ChatHistory.objects.create(
            user=self.other_user,
            note=other_note,
            question='Hidden question',
            answer='Hidden answer',
        )

        response = self.client.get(reverse('rag:chat'))

        self.assertContains(response, 'Visible question')
        self.assertNotContains(response, 'Hidden question')
