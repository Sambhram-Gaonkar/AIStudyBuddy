import fitz


def extract_pdf_pages(file_path):
    pages = []
    with fitz.open(file_path) as document:
        for page_index, page in enumerate(document, start=1):
            text = page.get_text('text').strip()
            if text:
                pages.append({'page_number': page_index, 'text': clean_text(text)})
    return pages


def clean_text(text):
    lines = [line.strip() for line in text.splitlines()]
    return ' '.join(line for line in lines if line)
