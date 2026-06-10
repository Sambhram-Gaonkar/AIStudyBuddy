def split_pages_into_chunks(pages, chunk_size=1000, overlap=150):
    chunks = []
    chunk_index = 0

    for page in pages:
        text = page['text']
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append({
                    'text': chunk_text,
                    'page_number': page['page_number'],
                    'chunk_index': chunk_index,
                })
                chunk_index += 1
            if end >= len(text):
                break
            start = max(end - overlap, start + 1)

    return chunks
