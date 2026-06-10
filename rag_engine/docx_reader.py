from docx import Document


def extract_docx_pages(file_path):
    document = Document(file_path)
    paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs]
    text = ' '.join(paragraph for paragraph in paragraphs if paragraph)
    if not text:
        return []
    return [{'page_number': None, 'text': text}]
