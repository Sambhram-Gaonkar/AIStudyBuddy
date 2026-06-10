# Tech Stack — AI Study Buddy

## 1. Backend

- Python
- Django
- Django Templates
- Django ORM

## 2. Database

MVP:

- SQLite

Later:

- PostgreSQL

## 3. Local LLM

Recommended:

- Ollama

Suggested models for low-end systems:

- `gemma3:1b`
- `llama3.2:1b`
- `phi3:mini`

Use smaller models first because the target local machine may have limited RAM/GPU.

## 4. Local Embeddings

Recommended:

- `nomic-embed-text` through Ollama

Alternative:

- Sentence Transformers:
  - `all-MiniLM-L6-v2`

## 5. Vector Store

Recommended for MVP:

- ChromaDB

Alternative:

- FAISS

## 6. PDF Extraction

Recommended:

- PyMuPDF

Alternative:

- pypdf

## 7. Quiz PDF Export

Beginner-friendly options:

- xhtml2pdf
- ReportLab

Recommended for simple Django HTML-to-PDF export:

- xhtml2pdf

## 8. Flashcard CSV Export

Use:

- Python `csv` module

Optional:

- pandas

## 9. Frontend

MVP:

- HTML
- CSS
- Bootstrap
- Django templates

Avoid React until the MVP is complete.

## 10. Development Tools

- VS Code
- Git
- GitHub
- Python virtual environment
- PowerShell or Command Prompt
- Ollama desktop/runtime

## 11. Suggested `requirements.txt`

```text
Django
pymupdf
chromadb
requests
xhtml2pdf
python-dotenv
```

If using sentence-transformers instead of Ollama embeddings:

```text
sentence-transformers
torch
```

## 12. Local Services

Ollama should run locally at:

```text
http://localhost:11434
```

This is acceptable because it is local machine communication.
