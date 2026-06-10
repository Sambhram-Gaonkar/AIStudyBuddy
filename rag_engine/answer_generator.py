from .llm_client import OllamaUnavailable, generate_text
from .vector_store import retrieve_chunks

NOT_FOUND_MESSAGE = 'I could not find this in your uploaded notes.'


def build_prompt(context, question):
    return f"""You are an AI study assistant.

Answer the student's question using only the provided notes.

If the answer is not present in the notes, say:
"{NOT_FOUND_MESSAGE}"

Keep the answer clear, simple, and student-friendly.

Notes:
{context}

Question:
{question}

Answer:
"""


def answer_question(user, note, question):
    matches, retrieval_mode = retrieve_chunks(user, note, question, top_k=5)
    if not matches:
        return {
            'answer': NOT_FOUND_MESSAGE,
            'sources': [],
            'retrieval_mode': retrieval_mode,
            'used_llm': False,
        }

    context = '\n\n'.join(match['text'] for match in matches)
    try:
        answer = generate_text(build_prompt(context, question))
        used_llm = True
    except OllamaUnavailable:
        answer = context[:1200].strip()
        used_llm = False

    sources = []
    for match in matches:
        metadata = match['metadata']
        sources.append({
            'note_title': metadata.get('note_title', note.title),
            'page_number': metadata.get('page_number') or 'Unknown',
            'chunk_index': metadata.get('chunk_index'),
        })

    return {
        'answer': answer or NOT_FOUND_MESSAGE,
        'sources': sources,
        'retrieval_mode': retrieval_mode,
        'used_llm': used_llm,
    }
