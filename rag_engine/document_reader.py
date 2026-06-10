from pathlib import Path

from .docx_reader import extract_docx_pages
from .pdf_reader import extract_pdf_pages


def extract_document_pages(file_path):
    extension = Path(file_path).suffix.lower()
    if extension == '.pdf':
        return extract_pdf_pages(file_path)
    if extension == '.docx':
        return extract_docx_pages(file_path)
    raise ValueError('Unsupported file type.')
