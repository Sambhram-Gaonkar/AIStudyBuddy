# Build Prompt for AI Coding Agent

You are building a local-only AI Study Buddy web application.

## Product Goal

Build a Django-based AI Study Buddy where students can upload PDF notes and use local AI to:

- Ask questions from uploaded notes using RAG
- Generate quizzes
- Export quizzes as PDF
- Generate flashcards
- Export flashcards as CSV
- Generate summaries
- View activity from a student dashboard

## Hard Requirement

The app must run locally. Do not use external AI APIs or cloud vector databases.

Do not use:

- OpenAI API
- Gemini API
- Anthropic API
- Pinecone
- Hosted LLM endpoints
- Cloud OCR
- Any feature that sends student notes outside the machine

Use local components:

- Django
- SQLite for MVP
- Ollama on localhost for LLM
- Local embedding model
- ChromaDB or FAISS for vector search
- PyMuPDF for PDF extraction
- ReportLab or xhtml2pdf for PDF export

## MVP Scope

Build these features only first:

1. Student authentication
2. Student dashboard
3. PDF note upload
4. PDF text extraction
5. Note chunking
6. Local embedding generation
7. Local vector search
8. RAG chatbot
9. Quiz generation
10. Quiz PDF export
11. Flashcard generation
12. Flashcard CSV export
13. Summary generation

## Development Rule

Before coding, read:

- `16_AGENT_RULES.md`
- `07_TASK_BOARD.md`
- `08_PROGRESS_LOG.md`
- `09_DECISION_LOG.md`

After coding, update:

- `07_TASK_BOARD.md`
- `08_PROGRESS_LOG.md`
- `10_CHANGELOG.md`

## Expected Style

Keep the code beginner-friendly and clean.

Use simple Django views/templates first. Do not jump to React unless the MVP is complete.

Prefer readable service files such as:

- `rag_engine/pdf_reader.py`
- `rag_engine/text_splitter.py`
- `rag_engine/vector_store.py`
- `rag_engine/llm_client.py`
- `rag_engine/answer_generator.py`
- `quiz/services.py`
- `flashcards/services.py`
- `summaries/services.py`

## Final App Behavior

A student should be able to:

1. Register/login
2. Upload a PDF
3. Ask questions about the PDF
4. Generate quiz questions from the PDF
5. Download quiz as PDF
6. Generate flashcards
7. Download flashcards as CSV
8. Generate a summary
9. See recent notes and activity on dashboard
