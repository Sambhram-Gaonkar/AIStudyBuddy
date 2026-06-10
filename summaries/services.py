import re

from rag_engine.llm_client import OllamaUnavailable, generate_text

from .models import Summary


def build_summary_prompt(note, summary_type):
    return f"""You are a study notes summarizer.

Create a {summary_type} summary from the notes below.

Use simple student-friendly language.
Use only the provided notes.

Notes:
{note.extracted_text[:6000]}
"""


def fallback_summary(note, summary_type):
    sentences = re.split(r'(?<=[.!?])\s+', note.extracted_text.strip())
    sentences = [sentence.strip() for sentence in sentences if len(sentence.strip()) > 20]
    selected = sentences[:6] or ['No clear text could be extracted from this note.']

    if summary_type == 'bullet':
        return '\n'.join(f'- {sentence}' for sentence in selected)
    if summary_type == 'exam':
        return '\n'.join(f'Exam point {index}: {sentence}' for index, sentence in enumerate(selected, start=1))
    return ' '.join(selected)


def generate_summary(user, note, summary_type):
    try:
        content = generate_text(build_summary_prompt(note, summary_type))
    except OllamaUnavailable:
        content = fallback_summary(note, summary_type)

    return Summary.objects.create(
        user=user,
        note=note,
        summary_type=summary_type,
        content=content,
    )
