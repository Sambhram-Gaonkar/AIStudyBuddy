import json
import re

from rag_engine.llm_client import OllamaUnavailable, generate_text

from .models import Quiz, QuizQuestion


def build_quiz_prompt(note, question_type, difficulty, number_of_questions):
    context = note.extracted_text[:5000]
    return f"""You are an exam question generator.

Create {number_of_questions} {question_type} questions from the notes below.

Difficulty: {difficulty}

Return only valid JSON in this shape:
[
  {{
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "correct_answer": "...",
    "explanation": "..."
  }}
]

Use an empty options array for non-MCQ questions.
Use only the provided notes.

Notes:
{context}
"""


def parse_llm_questions(text):
    start = text.find('[')
    end = text.rfind(']')
    if start == -1 or end == -1:
        raise ValueError('No JSON array found.')
    data = json.loads(text[start:end + 1])
    questions = []
    for item in data:
        questions.append({
            'question': str(item.get('question', '')).strip(),
            'options': item.get('options') or [],
            'correct_answer': str(item.get('correct_answer', '')).strip(),
            'explanation': str(item.get('explanation', '')).strip(),
        })
    return [question for question in questions if question['question']]


def fallback_questions(note, question_type, number_of_questions):
    sentences = re.split(r'(?<=[.!?])\s+', note.extracted_text.strip())
    sentences = [sentence.strip() for sentence in sentences if len(sentence.strip()) > 30]
    if not sentences:
        sentences = ['No clear sentence could be extracted from this note.']

    questions = []
    for index, sentence in enumerate(sentences[:number_of_questions], start=1):
        if question_type == 'mcq':
            questions.append({
                'question': f'Which statement is supported by the notes? ({index})',
                'options': [sentence, 'This is not covered in the notes.', 'The opposite is stated.', 'The notes do not mention this topic.'],
                'correct_answer': sentence,
                'explanation': 'This statement is taken from the uploaded note.',
            })
        elif question_type == 'true_false':
            questions.append({
                'question': f'True or False: {sentence}',
                'options': ['True', 'False'],
                'correct_answer': 'True',
                'explanation': 'This sentence appears in the uploaded note.',
            })
        else:
            questions.append({
                'question': f'Explain this point from the notes: {sentence[:120]}',
                'options': [],
                'correct_answer': sentence,
                'explanation': 'A complete answer should include this idea from the notes.',
            })
    return questions


def generate_quiz(user, note, question_type, difficulty, number_of_questions):
    try:
        response = generate_text(build_quiz_prompt(note, question_type, difficulty, number_of_questions))
        questions = parse_llm_questions(response)[:number_of_questions]
    except (OllamaUnavailable, ValueError, json.JSONDecodeError):
        questions = fallback_questions(note, question_type, number_of_questions)

    quiz = Quiz.objects.create(
        user=user,
        note=note,
        title=f'{note.title} Quiz',
        question_type=question_type,
        difficulty=difficulty,
    )
    for index, question_data in enumerate(questions, start=1):
        QuizQuestion.objects.create(
            quiz=quiz,
            question=question_data['question'],
            options=question_data['options'],
            correct_answer=question_data['correct_answer'],
            explanation=question_data['explanation'],
            order=index,
        )
    return quiz
