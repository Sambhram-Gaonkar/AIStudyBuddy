from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from notes.models import Note
from quiz.models import Quiz, QuizAttempt


class DashboardProgressTests(TestCase):
    def test_dashboard_calculates_attempt_metrics(self):
        user = get_user_model().objects.create_user(username='student', password='password123')
        note = Note.objects.create(
            user=user,
            title='Physics',
            file=SimpleUploadedFile('physics.pdf', b'%PDF-1.4'),
        )
        quiz = Quiz.objects.create(
            user=user,
            note=note,
            title='Physics quiz',
            question_type='mcq',
        )
        QuizAttempt.objects.create(
            user=user,
            quiz=quiz,
            score=3,
            total_questions=5,
        )
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard:home'))

        self.assertEqual(response.context['attempt_count'], 1)
        self.assertEqual(response.context['average_score'], 60)
        self.assertEqual(response.context['topic_performance'][0]['percentage'], 60)
