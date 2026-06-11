# Progress Log — AI Study Buddy

Use this file as the development diary.

Add new entries at the top.

Format:

```text
Date:
Agent:
Task IDs:
Summary:
Files Changed:
Testing Done:
Status:
Next Step:
```

---

## 2026-06-11

Agent: Codex
Task IDs: B006
Summary: Added user-owned subject folders, optional note subject assignment, subject creation page, note filtering, and subject labels.
Files Changed: notes/models.py, notes/forms.py, notes/views.py, notes/urls.py, notes/tests.py, notes/migrations/0002_subject_note_subject_and_more.py, templates/notes/list.html, templates/notes/detail.html, templates/notes/subject_form.html, static/css/styles.css, task/progress/changelog docs.
Testing Done: Ran `venv\Scripts\python.exe manage.py check`, applied notes migration, ran `venv\Scripts\python.exe manage.py test notes`, and ran Python compileall. Browser verification attempted but blocked by missing in-app virtual clipboard during login input.
Status: B006 finished.
Next Step: Backlog can continue with B007, PostgreSQL support.

---

## 2026-06-11

Agent: Codex
Task IDs: B005
Summary: Added note-specific flashcard revision flow, reveal-answer cards, know/review-again actions, cumulative review progress, mastery percentage, and completion screen.
Files Changed: flashcards/models.py, flashcards/views.py, flashcards/urls.py, flashcards/tests.py, flashcards/migrations/0002_flashcardprogress_and_more.py, templates/flashcards/list.html, templates/flashcards/revise.html, static/css/styles.css, task/progress/changelog docs.
Testing Done: Ran `venv\Scripts\python.exe manage.py check`, applied flashcard migration, ran `venv\Scripts\python.exe manage.py test flashcards`, ran Python compileall, and verified flashcard revision and 100% mastery completion in the in-app browser.
Status: B005 finished.
Next Step: Backlog can continue with B006, subject folders.

---

## 2026-06-11

Agent: Codex
Task IDs: B004
Summary: Added quiz attempt storage, take-quiz form, answer scoring, result review, percentage display, retry flow, and recent scores on quiz detail pages.
Files Changed: quiz/models.py, quiz/views.py, quiz/urls.py, quiz/tests.py, quiz/migrations/0002_quizattempt.py, templates/quiz/detail.html, templates/quiz/take.html, templates/quiz/attempt_result.html, static/css/styles.css, task/progress/changelog docs.
Testing Done: Ran `venv\Scripts\python.exe manage.py check`, applied quiz migration, ran `venv\Scripts\python.exe manage.py test quiz`, ran Python compileall, and verified login, quiz submission, and 100% score result in the in-app browser.
Status: B004 finished.
Next Step: Backlog can continue with B005, flashcard revision mode.

---

## 2026-06-10

Agent: Codex
Task IDs: B003
Summary: Added OCR-backed image note uploads for PNG, JPG, TIFF, and BMP files, routed image extraction through the shared document reader, and added upload error handling for missing OCR dependencies.
Files Changed: requirements.txt, notes/forms.py, notes/views.py, notes/tests.py, rag_engine/document_reader.py, rag_engine/image_reader.py, templates/notes/upload.html, templates/notes/list.html, templates/notes/detail.html, local setup/task/progress/changelog docs.
Testing Done: Ran `venv\Scripts\python.exe manage.py check`, `venv\Scripts\python.exe manage.py test notes`, and `python -m compileall notes rag_engine config`.
Status: B003 finished.
Next Step: Backlog can continue with B004, quiz score tracking.

---

## 2026-06-10

Agent: Codex
Task IDs: B002
Summary: Added PPTX upload support using local python-pptx extraction and routed PowerPoint uploads through the shared document reader before chunking and indexing.
Files Changed: requirements.txt, notes/forms.py, rag_engine/document_reader.py, rag_engine/pptx_reader.py, templates/notes/list.html, task/progress/changelog docs.
Testing Done: Ran `venv\Scripts\python.exe manage.py check`, ran Python compileall for notes/rag_engine/config, and ran a Django client smoke test that uploaded an in-memory PPTX, verified extracted text/chunking, and asked a RAG question against the uploaded PPTX.
Status: B002 finished.
Next Step: Backlog can continue with B003, OCR for image notes.

---

## 2026-06-10

Agent: Codex
Task IDs: B001
Summary: Added DOCX upload support using local python-docx extraction and routed PDF/DOCX uploads through a shared document reader before chunking and indexing.
Files Changed: requirements.txt, notes/forms.py, notes/views.py, rag_engine/docx_reader.py, rag_engine/document_reader.py, templates/dashboard/home.html, templates/notes/list.html, templates/notes/upload.html, task/progress/changelog docs.
Testing Done: Ran `venv\Scripts\python.exe manage.py check`, ran Python compileall for notes/rag_engine/config, and ran a Django client smoke test that uploaded an in-memory DOCX, verified extracted text/chunking, and asked a RAG question against the uploaded DOCX.
Status: B001 finished.
Next Step: Backlog can continue with B002, PPT upload.

---

## 2026-06-10

Agent: Codex
Task IDs: T028, T029, T030
Summary: Added recent quizzes, flashcards, and summaries to the dashboard, improved responsive local styling, and completed the full MVP smoke test.
Files Changed: dashboard/views.py, templates/dashboard/home.html, static/css/styles.css, task/progress/changelog/decision docs.
Testing Done: Ran `venv\Scripts\python.exe manage.py check`, ran Python compileall, ran complete MVP smoke test for upload, ask, quiz, PDF export, flashcards, CSV export, and summary generation, and verified the dashboard activity sections in the in-app browser.
Status: T028, T029, and T030 finished.
Next Step: MVP current sprint is complete. Backlog can start with B001 if expanding scope.

---

## 2026-06-10

Agent: Codex
Task IDs: T024, T025, T026, T027
Summary: Added summary model, generation form/pages, local LLM summary generation with offline fallback, list/detail pages, and dashboard summary counts.
Files Changed: summaries/, config/urls.py, dashboard/views.py, templates/base.html, templates/dashboard/home.html, templates/summaries/, task/progress/changelog docs.
Testing Done: Ran `venv\Scripts\python.exe manage.py check`, created and applied summaries migration, ran Python compileall, and ran a Django client smoke test that uploaded a PDF and generated bullet, paragraph, and exam-focused summaries.
Status: T024 through T027 finished.
Next Step: Start T028, add activity/recent items to dashboard.

---

## 2026-06-10

Agent: Codex
Task IDs: T021, T022, T023
Summary: Added flashcard model, generation form/pages, local LLM flashcard generation with offline fallback, flashcard list, dashboard counts, and CSV export.
Files Changed: flashcards/, config/urls.py, dashboard/views.py, templates/base.html, templates/dashboard/home.html, templates/flashcards/, static/css/styles.css, task/progress/changelog docs.
Testing Done: Ran `venv\Scripts\python.exe manage.py check`, created and applied flashcards migration, ran Python compileall, and ran a Django client smoke test that uploaded a PDF, generated flashcards, opened the flashcard list, and exported CSV.
Status: T021 through T023 finished.
Next Step: Start T024, summary model.

---

## 2026-06-10

Agent: Codex
Task IDs: T016, T017, T018, T019, T020
Summary: Added quiz models, quiz generation form/pages, local LLM quiz generation with offline fallback, quiz detail/list views, dashboard quiz counts, and PDF export through xhtml2pdf.
Files Changed: quiz/, config/urls.py, dashboard/views.py, templates/base.html, templates/dashboard/home.html, templates/quiz/, static/css/styles.css, task/progress/changelog/decision docs.
Testing Done: Ran `venv\Scripts\python.exe manage.py check`, created and applied quiz migration, ran Python compileall, ran a Django client smoke test that uploaded a PDF, generated an MCQ quiz, opened the detail page, and exported a PDF, and verified the Generate Quiz page in the in-app browser.
Status: T016 through T020 finished.
Next Step: Start T021, flashcard model.

---

## 2026-06-10

Agent: Codex
Task IDs: T009, T010, T011, T012, T013, T014, T015
Summary: Added local ChromaDB vector store configuration, Ollama embedding/text generation clients, chunk indexing after upload, authenticated RAG chat page, retrieval logic, local LLM answer generation, and not-found fallback behavior.
Files Changed: config/settings.py, config/urls.py, notes/views.py, rag/, rag_engine/, templates/base.html, templates/dashboard/home.html, templates/rag/chat.html, static/css/styles.css, task/progress/changelog/decision docs.
Testing Done: Ran `venv\Scripts\python.exe manage.py check`, ran Python compileall, ran a Django client RAG smoke test with an uploaded in-memory PDF, verified relevant questions return note text when Ollama is offline, verified unrelated questions return the required not-found message, and verified the Ask AI page in the in-app browser after login.
Status: T009 through T015 finished.
Next Step: Start T016, quiz models.

---

## 2026-06-10

Agent: Codex
Task IDs: T004, T005, T006, T007, T008
Summary: Added authenticated dashboard counts and quick actions, user-owned Note and NoteChunk models, PDF upload/list/detail pages, local PyMuPDF extraction, and text chunking.
Files Changed: notes/, dashboard/views.py, config/settings.py, config/urls.py, rag_engine/, templates/dashboard/, templates/notes/, static/css/styles.css, task/progress/changelog docs.
Testing Done: Ran `venv\Scripts\python.exe manage.py check`, created and applied notes migration, ran a Django client smoke test that uploaded an in-memory PDF and verified extracted text and chunk creation, verified live login page returns 200 and dashboard redirects unauthenticated users to login.
Status: T004, T005, T006, T007, and T008 finished.
Next Step: Start T009, local vector store configuration.

---

## 2026-06-10

Agent: Codex
Task IDs: T003
Summary: Added accounts URLs, registration form/view, login/logout routes using Django auth, and login/register templates with navigation that reflects authentication state.
Files Changed: accounts/, config/urls.py, templates/base.html, templates/accounts/, static/css/styles.css, task/progress/changelog docs.
Testing Done: Ran `venv\Scripts\python.exe manage.py check`, verified `/accounts/login/`, `/accounts/register/`, and `/` return HTTP 200 on port 8001, and confirmed the auth pages render in the browser.
Status: T003 finished.
Next Step: Start T004, student dashboard page.

---

## 2026-06-10

Agent: Codex
Task IDs: T001, T002
Summary: Created the Django project scaffold, added MVP app modules, configured templates/static/media settings, added requirements.txt, created a virtual environment, and installed dependencies locally.
Files Changed: manage.py, config/, accounts/, dashboard/, notes/, rag/, quiz/, flashcards/, summaries/, templates/, static/, requirements.txt, .gitignore, task/progress/changelog docs.
Testing Done: Ran `venv\Scripts\python.exe manage.py check`, ran migrations, started the app on `http://127.0.0.1:8001/`, and verified the homepage rendered in the browser. Port 8000 was already used by another Django project.
Status: T001 and T002 finished.
Next Step: Start T003, accounts app with login/register/logout.

---

## 2026-06-10

Agent: Initial Planning
Task IDs: Setup
Summary: Created project planning documentation for local-only AI Study Buddy MVP.
Files Changed: Agent documentation markdown files created.
Testing Done: Not applicable.
Status: Planning created.
Next Step: Start with T001 and T002 from `07_TASK_BOARD.md`.
