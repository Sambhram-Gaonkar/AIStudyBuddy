from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from rag_engine.document_reader import extract_document_pages
from rag_engine.image_reader import OCRUnavailable

from .forms import NoteUploadForm
from .models import Note, NoteChunk, Subject


class NoteUploadFormTests(TestCase):
    def test_accepts_image_note_upload(self):
        uploaded_file = SimpleUploadedFile(
            'whiteboard.png',
            b'image-bytes',
            content_type='image/png',
        )

        form = NoteUploadForm(data={'title': 'Whiteboard'}, files={'file': uploaded_file})

        self.assertTrue(form.is_valid(), form.errors)

    def test_rejects_unsupported_upload_type(self):
        uploaded_file = SimpleUploadedFile(
            'notes.txt',
            b'plain text',
            content_type='text/plain',
        )

        form = NoteUploadForm(data={'title': 'Text'}, files={'file': uploaded_file})

        self.assertFalse(form.is_valid())
        self.assertIn('Only PDF, DOCX, PPTX, and image files are supported.', form.errors['file'])

    def test_accepts_generic_browser_content_type_for_supported_extension(self):
        uploaded_file = SimpleUploadedFile(
            'notes.pdf',
            b'%PDF-1.4 data',
            content_type='application/octet-stream',
        )

        form = NoteUploadForm(data={'title': 'Browser PDF'}, files={'file': uploaded_file})

        self.assertTrue(form.is_valid(), form.errors)

    def test_rejects_empty_file(self):
        uploaded_file = SimpleUploadedFile('empty.pdf', b'', content_type='application/pdf')

        form = NoteUploadForm(data={'title': 'Empty'}, files={'file': uploaded_file})

        self.assertFalse(form.is_valid())
        self.assertIn('empty', form.errors['file'][0].lower())


class DocumentReaderTests(TestCase):
    @patch('rag_engine.document_reader.extract_image_pages')
    def test_routes_image_files_to_ocr_reader(self, mock_extract_image_pages):
        mock_extract_image_pages.return_value = [{'page_number': 1, 'text': 'OCR text'}]

        pages = extract_document_pages('scan.jpg')

        self.assertEqual(pages, [{'page_number': 1, 'text': 'OCR text'}])
        mock_extract_image_pages.assert_called_once_with('scan.jpg')


class NoteUploadViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='student',
            password='pass12345',
        )
        self.client.force_login(self.user)

    def tearDown(self):
        for note in Note.objects.all():
            if note.file:
                note.file.delete(save=False)

    @patch('notes.views.index_note_chunks')
    @patch('notes.views.extract_document_pages')
    def test_upload_image_note_extracts_and_chunks_ocr_text(self, mock_extract_document_pages, mock_index_note_chunks):
        mock_extract_document_pages.return_value = [
            {'page_number': 1, 'text': 'Photosynthesis converts light into chemical energy.'},
        ]
        uploaded_file = SimpleUploadedFile(
            'test-ocr-board.png',
            b'image-bytes',
            content_type='image/png',
        )

        response = self.client.post(
            reverse('notes:upload'),
            {'title': 'Board Notes', 'file': uploaded_file},
        )

        note = Note.objects.get(title='Board Notes')
        self.assertRedirects(response, reverse('notes:detail', kwargs={'pk': note.pk}))
        self.assertEqual(note.extracted_text, 'Photosynthesis converts light into chemical energy.')
        self.assertEqual(NoteChunk.objects.filter(note=note).count(), 1)
        mock_index_note_chunks.assert_called_once_with(note)

    @patch('notes.views.extract_document_pages')
    def test_upload_image_note_shows_error_when_ocr_is_unavailable(self, mock_extract_document_pages):
        mock_extract_document_pages.side_effect = OCRUnavailable('Tesseract OCR is not installed or is not available on PATH.')
        uploaded_file = SimpleUploadedFile(
            'test-ocr-board.png',
            b'image-bytes',
            content_type='image/png',
        )

        response = self.client.post(
            reverse('notes:upload'),
            {'title': 'Board Notes', 'file': uploaded_file},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tesseract OCR is not installed or is not available on PATH.')
        self.assertFalse(Note.objects.filter(title='Board Notes').exists())

    @patch('notes.views.extract_document_pages')
    def test_upload_rejects_document_without_readable_text(self, mock_extract_document_pages):
        mock_extract_document_pages.return_value = []
        uploaded_file = SimpleUploadedFile(
            'blank.pdf',
            b'%PDF-1.4 blank',
            content_type='application/pdf',
        )

        response = self.client.post(
            reverse('notes:upload'),
            {'title': 'Blank Notes', 'file': uploaded_file},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No readable text was found in this file.')
        self.assertFalse(Note.objects.filter(title='Blank Notes').exists())

    def test_upload_invalid_document_shows_read_error(self):
        uploaded_file = SimpleUploadedFile(
            'broken.pdf',
            b'not a real pdf',
            content_type='application/pdf',
        )

        response = self.client.post(
            reverse('notes:upload'),
            {'title': 'Broken Notes', 'file': uploaded_file},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This file could not be read.')
        self.assertFalse(Note.objects.filter(title='Broken Notes').exists())


class SubjectFolderTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='subject-student',
            password='pass12345',
        )
        self.other_user = get_user_model().objects.create_user(
            username='other-subject-student',
            password='pass12345',
        )
        self.client.force_login(self.user)

    def test_create_subject_for_current_user(self):
        response = self.client.post(reverse('notes:create_subject'), {'name': 'Physics'})

        self.assertRedirects(response, reverse('notes:list'))
        self.assertTrue(Subject.objects.filter(user=self.user, name='Physics').exists())

    def test_upload_form_only_lists_current_users_subjects(self):
        own_subject = Subject.objects.create(user=self.user, name='Biology')
        Subject.objects.create(user=self.other_user, name='Private')

        form = NoteUploadForm(user=self.user)

        self.assertQuerySetEqual(form.fields['subject'].queryset, [own_subject])

    def test_note_list_filters_by_owned_subject(self):
        subject = Subject.objects.create(user=self.user, name='Chemistry')
        Note.objects.create(user=self.user, subject=subject, title='Atoms', file='notes/atoms.pdf')
        Note.objects.create(user=self.user, title='General', file='notes/general.pdf')

        response = self.client.get(reverse('notes:list'), {'subject': subject.pk})

        self.assertContains(response, 'Atoms')
        self.assertNotContains(response, 'General')
