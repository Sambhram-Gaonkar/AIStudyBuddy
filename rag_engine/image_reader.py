import os
from pathlib import Path

SUPPORTED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp'}


class OCRUnavailable(Exception):
    pass


def extract_image_pages(file_path):
    try:
        from PIL import Image
        import pytesseract
    except ImportError as exc:
        raise OCRUnavailable('Install Pillow, pytesseract, and the Tesseract OCR engine to process image notes.') from exc

    configure_tesseract(pytesseract)

    try:
        with Image.open(file_path) as image:
            text = pytesseract.image_to_string(image).strip()
    except pytesseract.TesseractNotFoundError as exc:
        raise OCRUnavailable('Tesseract OCR is not installed or is not available on PATH.') from exc

    cleaned_text = clean_text(text)
    if not cleaned_text:
        return []
    return [{'page_number': 1, 'text': cleaned_text}]


def clean_text(text):
    lines = [line.strip() for line in text.splitlines()]
    return ' '.join(line for line in lines if line)


def configure_tesseract(pytesseract):
    local_app_data = os.environ.get('LOCALAPPDATA')
    candidate_paths = []
    if local_app_data:
        candidate_paths.append(Path(local_app_data) / 'Programs' / 'Tesseract-OCR' / 'tesseract.exe')
    candidate_paths.extend([
        Path('C:/Program Files/Tesseract-OCR/tesseract.exe'),
        Path('C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'),
    ])

    for path in candidate_paths:
        if path.exists():
            pytesseract.pytesseract.tesseract_cmd = str(path)
            return
