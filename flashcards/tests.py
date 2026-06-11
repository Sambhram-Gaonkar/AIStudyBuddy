from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

from .models import Flashcard, FlashcardProgress


class FlashcardRevisionTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='flash-student',
            password='pass12345',
        )
        self.other_user = get_user_model().objects.create_user(
            username='other-flash-student',
            password='pass12345',
        )
        self.note = Note.objects.create(
            user=self.user,
            title='Biology',
            file='notes/biology.pdf',
            extracted_text='Cells are the basic unit of life.',
        )
        self.card = Flashcard.objects.create(
            user=self.user,
            note=self.note,
            front='Cell',
            back='Basic unit of life',
        )
        self.client.force_login(self.user)

    def test_mark_known_updates_progress_and_advances(self):
        response = self.client.post(
            reverse('flashcards:revise', kwargs={'note_id': self.note.pk}),
            {'result': 'known'},
        )

        progress = FlashcardProgress.objects.get(user=self.user, flashcard=self.card)
        self.assertEqual(progress.review_count, 1)
        self.assertEqual(progress.known_count, 1)
        self.assertEqual(progress.mastery_percentage, 100)
        self.assertRedirects(
            response,
            f"{reverse('flashcards:revise', kwargs={'note_id': self.note.pk})}?position=1",
        )

    def test_user_cannot_revise_another_users_note(self):
        self.client.force_login(self.other_user)

        response = self.client.get(reverse('flashcards:revise', kwargs={'note_id': self.note.pk}))

        self.assertEqual(response.status_code, 404)
