# AI Study Buddy

Local-first Django study assistant. Upload PDF, DOCX, PPTX, or image notes. Ask grounded questions, generate quizzes, revise flashcards, and create summaries without cloud AI APIs.

## Quick Start

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8001
```

Open `http://127.0.0.1:8001/`.

## Local AI

Install Ollama, then:

```powershell
ollama pull gemma3:1b
ollama pull nomic-embed-text
```

Without Ollama, retrieval and generators use local fallback behavior.

## Optional Features

- Image OCR requires Tesseract OCR.
- PostgreSQL uses `.env` settings from `.env.example`.
- Production-like local serving uses Waitress and WhiteNoise.

See `ai_study_buddy_agent_docs/11_LOCAL_SETUP.md` and `ai_study_buddy_agent_docs/18_DEPLOYMENT_GUIDE.md`.
