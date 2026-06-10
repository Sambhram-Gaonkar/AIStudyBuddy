import json
import re

from rag_engine.llm_client import OllamaUnavailable, generate_text

from .models import Flashcard


def build_flashcard_prompt(note, number_of_cards):
    return f"""You are a flashcard generator.

Create {number_of_cards} key term and definition flashcards from the notes below.

Return only valid JSON in this shape:
[
  {{"front": "term or question", "back": "definition or answer"}}
]

Use only the provided notes.

Notes:
{note.extracted_text[:5000]}
"""


def parse_flashcards(text):
    start = text.find('[')
    end = text.rfind(']')
    if start == -1 or end == -1:
        raise ValueError('No JSON array found.')
    data = json.loads(text[start:end + 1])
    cards = []
    for item in data:
        front = str(item.get('front', '')).strip()
        back = str(item.get('back', '')).strip()
        if front and back:
            cards.append({'front': front, 'back': back})
    return cards


def fallback_flashcards(note, number_of_cards):
    sentences = re.split(r'(?<=[.!?])\s+', note.extracted_text.strip())
    sentences = [sentence.strip() for sentence in sentences if len(sentence.strip()) > 30]
    cards = []
    for index, sentence in enumerate(sentences[:number_of_cards], start=1):
        words = re.findall(r'[A-Za-z][A-Za-z0-9-]+', sentence)
        front = words[0] if words else f'Key idea {index}'
        cards.append({
            'front': front,
            'back': sentence,
        })
    return cards


def generate_flashcards(user, note, number_of_cards):
    try:
        response = generate_text(build_flashcard_prompt(note, number_of_cards))
        cards = parse_flashcards(response)[:number_of_cards]
    except (OllamaUnavailable, ValueError, json.JSONDecodeError):
        cards = fallback_flashcards(note, number_of_cards)

    Flashcard.objects.filter(user=user, note=note).delete()
    return [
        Flashcard.objects.create(
            user=user,
            note=note,
            front=card['front'],
            back=card['back'],
        )
        for card in cards
    ]
