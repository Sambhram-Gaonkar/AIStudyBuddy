from unittest.mock import patch

import fitz
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from flashcards.models import Flashcard
from quiz.models import Quiz, QuizAttempt
from rag.models import ChatHistory
from rag_engine.llm_client import OllamaUnavailable
from summaries.models import Summary

from .models import Note


class FullOfflineWorkflowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='workflow-student',
            password='pass12345',
        )
        self.client.force_login(self.user)

    def tearDown(self):
        for note in Note.objects.filter(user=self.user):
            if note.file:
                note.file.delete(save=False)

    def make_pdf(self):
        document = fitz.open()
        page = document.new_page()
        page.insert_text(
            (72, 72),
            (
                'Photosynthesis converts sunlight into chemical energy. '
                'Chlorophyll captures light inside plant cells. '
                'Plants release oxygen during this process.'
            ),
        )
        content = document.tobytes()
        document.close()
        return content

    def test_complete_study_flow_works_without_ollama(self):
        upload = SimpleUploadedFile(
            'workflow-biology.pdf',
            self.make_pdf(),
            content_type='application/pdf',
        )
        with patch('notes.views.index_note_chunks', side_effect=OllamaUnavailable()):
            response = self.client.post(
                reverse('notes:upload'),
                {'title': 'Biology', 'file': upload},
            )

        note = Note.objects.get(user=self.user, title='Biology')
        self.assertRedirects(response, reverse('notes:detail', kwargs={'pk': note.pk}))
        self.assertTrue(note.extracted_text)
        self.assertTrue(note.chunks.exists())

        with (
            patch('rag_engine.vector_store.search_note_chunks', side_effect=OllamaUnavailable()),
            patch('rag_engine.answer_generator.generate_text', side_effect=OllamaUnavailable()),
        ):
            response = self.client.post(
                reverse('rag:chat'),
                {'note': note.pk, 'question': 'What converts sunlight into chemical energy?'},
            )
        self.assertContains(response, 'Photosynthesis converts sunlight')
        self.assertTrue(ChatHistory.objects.filter(user=self.user, note=note).exists())

        with patch('quiz.services.generate_text', side_effect=OllamaUnavailable()):
            response = self.client.post(
                reverse('quiz:generate'),
                {
                    'note': note.pk,
                    'question_type': 'mcq',
                    'difficulty': 'medium',
                    'number_of_questions': 3,
                },
            )
        quiz = Quiz.objects.get(user=self.user, note=note)
        self.assertRedirects(response, reverse('quiz:detail', kwargs={'pk': quiz.pk}))
        self.assertEqual(quiz.questions.count(), 3)

        answers = {
            f'question_{question.pk}': question.correct_answer
            for question in quiz.questions.all()
        }
        response = self.client.post(reverse('quiz:take', kwargs={'pk': quiz.pk}), answers)
        attempt = QuizAttempt.objects.get(user=self.user, quiz=quiz)
        self.assertRedirects(response, reverse('quiz:attempt_result', kwargs={'pk': attempt.pk}))
        self.assertEqual(attempt.percentage, 100)

        response = self.client.get(reverse('quiz:pdf', kwargs={'pk': quiz.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response.content.startswith(b'%PDF'))

        with patch('flashcards.services.generate_text', side_effect=OllamaUnavailable()):
            response = self.client.post(
                reverse('flashcards:generate'),
                {'note': note.pk, 'number_of_cards': 4},
            )
        self.assertRedirects(response, reverse('flashcards:list'))
        self.assertEqual(Flashcard.objects.filter(user=self.user, note=note).count(), 4)

        response = self.client.get(reverse('flashcards:csv', kwargs={'note_id': note.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn(b'Term,Definition', response.content)

        with patch('summaries.services.generate_text', side_effect=OllamaUnavailable()):
            response = self.client.post(
                reverse('summaries:generate'),
                {'note': note.pk, 'summary_type': 'bullet'},
            )
        summary = Summary.objects.get(user=self.user, note=note)
        self.assertRedirects(response, reverse('summaries:detail', kwargs={'pk': summary.pk}))
        self.assertIn('Photosynthesis', summary.content)
