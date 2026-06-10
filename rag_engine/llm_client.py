import requests
from django.conf import settings


class OllamaUnavailable(Exception):
    pass


def generate_embedding(text):
    try:
        response = requests.post(
            f'{settings.OLLAMA_BASE_URL}/api/embeddings',
            json={'model': settings.OLLAMA_EMBED_MODEL, 'prompt': text},
            timeout=30,
        )
    except requests.RequestException as exc:
        raise OllamaUnavailable('Ollama embedding model is not available.') from exc
    if response.status_code != 200:
        raise OllamaUnavailable('Ollama embedding model is not available.')
    data = response.json()
    embedding = data.get('embedding')
    if not embedding:
        raise OllamaUnavailable('Ollama did not return an embedding.')
    return embedding


def generate_text(prompt):
    try:
        response = requests.post(
            f'{settings.OLLAMA_BASE_URL}/api/generate',
            json={
                'model': settings.OLLAMA_CHAT_MODEL,
                'prompt': prompt,
                'stream': False,
            },
            timeout=120,
        )
    except requests.RequestException as exc:
        raise OllamaUnavailable('Ollama chat model is not available.') from exc
    if response.status_code != 200:
        raise OllamaUnavailable('Ollama chat model is not available.')
    data = response.json()
    answer = data.get('response', '').strip()
    if not answer:
        raise OllamaUnavailable('Ollama did not return an answer.')
    return answer
