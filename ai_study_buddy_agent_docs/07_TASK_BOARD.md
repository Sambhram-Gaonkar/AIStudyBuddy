# Task Board — AI Study Buddy

Use this file to track all tasks.

Allowed status values:

- Pending
- In Progress
- Blocked
- Finished

## Current Sprint

| ID | Task | Priority | Status | Notes |
|---|---|---:|---|---|
| T001 | Create Django project and base config | High | Finished | Django project, base apps, templates, static/media settings, and root route created |
| T002 | Create virtual environment and requirements.txt | High | Finished | Virtual environment created and dependencies installed from requirements.txt |
| T003 | Create accounts app with login/register/logout | High | Finished | Django auth login/logout plus registration view added |
| T004 | Create student dashboard page | High | Finished | Shows counts, recent notes, and quick actions |
| T005 | Create notes app and Note model | High | Finished | Note and NoteChunk are user-owned |
| T006 | Add PDF upload form and view | High | Finished | PDF upload saves files under media |
| T007 | Extract text from PDF locally | High | Finished | Uses PyMuPDF through rag_engine/pdf_reader.py |
| T008 | Split extracted text into chunks | High | Finished | Uses 1000 character chunks with 150 character overlap |
| T009 | Configure local vector store | High | Finished | ChromaDB PersistentClient configured under chroma_db |
| T010 | Generate local embeddings | High | Finished | Uses Ollama nomic-embed-text through localhost |
| T011 | Store note chunks in vector store | High | Finished | Upload flow indexes chunks with user/note/page metadata when Ollama is available |
| T012 | Build RAG chatbot page | High | Finished | Authenticated Ask AI page selects a note and question |
| T013 | Retrieve matching chunks for question | High | Finished | Retrieves top matches from ChromaDB with keyword fallback |
| T014 | Generate answer using local LLM | High | Finished | Uses Ollama localhost generate endpoint when available |
| T015 | Add fallback when answer not found | Medium | Finished | Returns required not-found message for unrelated questions |
| T016 | Create quiz models | High | Finished | Quiz and QuizQuestion models added |
| T017 | Generate MCQ quiz from notes | High | Finished | Stores generated MCQ quizzes |
| T018 | Generate True/False quiz from notes | Medium | Finished | Stores generated true/false quizzes |
| T019 | Generate short answer questions from notes | Medium | Finished | Stores generated short-answer quizzes |
| T020 | Export quiz as PDF | High | Finished | Uses xhtml2pdf to export stored quizzes |
| T021 | Create flashcard model | High | Finished | Front/back Flashcard model added |
| T022 | Generate flashcards from notes | High | Finished | Stores generated cards for each note |
| T023 | Export flashcards as CSV | High | Finished | Uses Python csv module |
| T024 | Create summary model | High | Finished | Summary model stores summary type |
| T025 | Generate bullet summary | High | Finished | Generates from selected note |
| T026 | Generate paragraph summary | Medium | Finished | Generates from selected note |
| T027 | Generate exam-focused summary | Medium | Finished | Generates from selected note |
| T028 | Add activity/recent items to dashboard | Medium | Finished | Recent notes, quizzes, flashcards, and summaries |
| T029 | Add basic UI styling | Medium | Finished | Local responsive CSS used for MVP styling |
| T030 | Test complete MVP flow | High | Finished | Upload → Ask → Quiz → PDF → Flashcards → CSV → Summary smoke test passed |

## Backlog

| ID | Task | Priority | Status | Notes |
|---|---|---:|---|---|
| B001 | Add DOCX upload | Low | Finished | Local DOCX text extraction added |
| B002 | Add PPT upload | Low | Finished | Local PPTX text extraction added |
| B003 | Add OCR for image notes | Low | Finished | Supports PNG, JPG, TIFF, and BMP uploads through pytesseract |
| B004 | Add quiz score tracking | Low | Finished | Quiz attempts store answers, score, and percentage |
| B005 | Add flashcard revision mode | Low | Finished | Tracks reviews, known answers, and mastery |
| B006 | Add subject folders | Low | Finished | User-owned subjects, upload assignment, and note filtering |
| B007 | Add PostgreSQL support | Low | Finished | Optional env-based PostgreSQL config; SQLite remains default |
| B008 | Add deployment guide | Low | Finished | Waitress, WhiteNoise, environment security settings, and local/LAN deployment steps documented |
| B009 | Add Ask AI chat history | Low | Finished | Persists user-owned questions, answers, retrieval details, and source metadata |
