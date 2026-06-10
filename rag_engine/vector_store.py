import chromadb
import re
from django.conf import settings

from .llm_client import OllamaUnavailable, generate_embedding

STOPWORDS = {
    'about', 'after', 'again', 'also', 'and', 'are', 'can', 'did', 'does',
    'for', 'from', 'has', 'have', 'how', 'into', 'the', 'this', 'was',
    'what', 'when', 'where', 'which', 'who', 'why', 'with',
}


def get_collection():
    client = chromadb.PersistentClient(path=str(settings.CHROMA_DB_DIR))
    return client.get_or_create_collection(name=settings.CHROMA_COLLECTION_NAME)


def chunk_document_id(chunk):
    return f'note-{chunk.note_id}-chunk-{chunk.chunk_index}'


def index_note_chunks(note):
    chunks = list(note.chunks.all())
    if not chunks:
        return 0

    collection = get_collection()
    documents = []
    embeddings = []
    metadatas = []
    ids = []

    for chunk in chunks:
        documents.append(chunk.text)
        embeddings.append(generate_embedding(chunk.text))
        metadatas.append({
            'user_id': str(chunk.user_id),
            'note_id': str(chunk.note_id),
            'note_title': note.title,
            'page_number': chunk.page_number or 0,
            'chunk_index': chunk.chunk_index,
        })
        ids.append(chunk_document_id(chunk))

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    return len(chunks)


def search_note_chunks(user, note, question, top_k=5):
    question_embedding = generate_embedding(question)
    collection = get_collection()
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
        where={
            '$and': [
                {'user_id': {'$eq': str(user.id)}},
                {'note_id': {'$eq': str(note.id)}},
            ]
        },
        include=['documents', 'metadatas', 'distances'],
    )
    documents = results.get('documents', [[]])[0]
    metadatas = results.get('metadatas', [[]])[0]
    distances = results.get('distances', [[]])[0]
    matches = []
    for document, metadata, distance in zip(documents, metadatas, distances):
        matches.append({
            'text': document,
            'metadata': metadata,
            'distance': distance,
        })
    return matches


def lexical_search_note_chunks(note, question, top_k=5):
    terms = set(re.findall(r'[a-zA-Z0-9]+', question.lower()))
    terms = {term for term in terms if len(term) > 2 and term not in STOPWORDS}
    scored_chunks = []

    for chunk in note.chunks.all():
        text_terms = set(re.findall(r'[a-zA-Z0-9]+', chunk.text.lower()))
        score = len(terms & text_terms)
        if score:
            scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda item: item[0], reverse=True)
    return [
        {
            'text': chunk.text,
            'metadata': {
                'user_id': str(chunk.user_id),
                'note_id': str(chunk.note_id),
                'note_title': note.title,
                'page_number': chunk.page_number or 0,
                'chunk_index': chunk.chunk_index,
            },
            'distance': None,
        }
        for score, chunk in scored_chunks[:top_k]
    ]


def retrieve_chunks(user, note, question, top_k=5):
    try:
        matches = search_note_chunks(user, note, question, top_k=top_k)
        if matches:
            return matches, 'vector'
    except (OllamaUnavailable, Exception):
        pass

    return lexical_search_note_chunks(note, question, top_k=top_k), 'keyword'
