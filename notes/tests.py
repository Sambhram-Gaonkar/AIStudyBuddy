from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from rag_engine.document_reader import extract_document_pages
from rag_engine.image_reader import OCRUnavailable

from .forms import NoteUploadForm
from .models import Note, NoteChunk


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
