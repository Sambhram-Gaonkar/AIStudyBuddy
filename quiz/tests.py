from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

from .models import Quiz, QuizAttempt, QuizQuestion
from .services import fallback_questions


class QuizScoreTrackingTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='quiz-student',
            password='pass12345',
        )
        self.other_user = get_user_model().objects.create_user(
            username='other-student',
            password='pass12345',
        )
        self.note = Note.objects.create(
            user=self.user,
            title='Physics',
            file='notes/physics.pdf',
            extracted_text='Gravity pulls objects toward Earth.',
        )
        self.quiz = Quiz.objects.create(
            user=self.user,
            note=self.note,
            title='Physics Quiz',
            question_type='mcq',
            difficulty='easy',
        )
        self.question = QuizQuestion.objects.create(
            quiz=self.quiz,
            question='What pulls objects toward Earth?',
            options=['Gravity', 'Friction'],
            correct_answer='Gravity',
            explanation='Gravity attracts objects.',
            order=1,
        )
        self.client.force_login(self.user)

    def test_submit_quiz_creates_scored_attempt(self):
        response = self.client.post(
            reverse('quiz:take', kwargs={'pk': self.quiz.pk}),
            {f'question_{self.question.pk}': 'Gravity'},
        )

        attempt = QuizAttempt.objects.get(user=self.user, quiz=self.quiz)
        self.assertRedirects(response, reverse('quiz:attempt_result', kwargs={'pk': attempt.pk}))
        self.assertEqual(attempt.score, 1)
        self.assertEqual(attempt.total_questions, 1)
        self.assertEqual(attempt.percentage, 100)

    def test_user_cannot_take_another_users_quiz(self):
        self.client.force_login(self.other_user)

        response = self.client.get(reverse('quiz:take', kwargs={'pk': self.quiz.pk}))

        self.assertEqual(response.status_code, 404)

    def test_offline_fallback_creates_requested_question_count(self):
        questions = fallback_questions(self.note, 'mcq', 4)

        self.assertEqual(len(questions), 4)
        self.assertTrue(all(question['options'] for question in questions))
