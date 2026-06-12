# Decision Log — AI Study Buddy

Use this file to record technical decisions.

Add new decisions at the top.

Format:

```text
Date:
Decision:
Reason:
Alternatives Considered:
Impact:
```

---

## 2026-06-12

### Decision: Keep every study workflow usable when Ollama is unavailable

Reason:
Local model setup is optional and may not be running. Upload, retrieval, quiz, flashcard, and summary workflows must still complete without server errors.

Alternatives Considered:

- Require Ollama before allowing AI study actions
- Disable generators while the model is offline

Impact:
Database-backed keyword retrieval and deterministic generators remain available offline. Ollama improves generated content when installed, but it is not a runtime requirement for core workflows.

---

## 2026-06-12

### Decision: Implement the Stitch design with local CSS and existing Django data

Reason:
The provided design defines an academic minimalist visual system, but its exported HTML depends on Tailwind, Google Fonts, remote images, and mock data. The app must stay local-first and preserve existing Django workflows.

Alternatives Considered:

- Copy the exported Tailwind HTML directly
- Load fonts, icons, and images from external CDNs
- Apply only palette changes without restructuring pages

Impact:
The app now follows the supplied layout, spacing, color, and component direction using one local stylesheet, system fonts, real database metrics, and existing routes. No new cloud frontend dependency was introduced.

---

## 2026-06-11

### Decision: Store Ask AI history in Django with JSON source metadata

Reason:
Questions and answers need durable, user-owned local history. Source details vary by retrieval result, so a JSON field preserves page and chunk metadata without another table.

Alternatives Considered:

- Keep history only in the browser session
- Create a separate relational source table
- Store chat history in ChromaDB

Impact:
Each valid Ask AI request creates a local database record linked to its user and note. The page can show recent history while keeping other users' questions private.

---

## 2026-06-10

### Decision: Use local CSS instead of external Bootstrap assets

Reason:
The app is local-first and should not depend on external CDN assets to render the MVP. The existing local stylesheet provides the basic Bootstrap-like layout needs for the current sprint.

Alternatives Considered:

- Load Bootstrap from a CDN
- Vendor the full Bootstrap distribution manually

Impact:
The UI works offline and avoids third-party asset requests. If exact Bootstrap components are required later, Bootstrap can be vendored into `static/` without changing backend behavior.

---

## 2026-06-10

### Decision: Add deterministic local fallback quiz generation

Reason:
Quiz generation should remain testable when Ollama is not running. The fallback uses extracted note sentences to create simple stored questions without sending content outside the machine.

Alternatives Considered:

- Require Ollama for quiz generation
- Block quiz generation when the local model is offline

Impact:
The quiz workflow, database storage, and PDF export can be developed and tested offline, while Ollama provides better generated questions when available.

---

## 2026-06-10

### Decision: Use keyword retrieval as an offline fallback for RAG

Reason:
Ollama may not be running during local development. The app should remain usable and return a clear not-found response instead of crashing when embeddings or answer generation are unavailable.

Alternatives Considered:

- Require Ollama for every chat request
- Disable the chat page when Ollama is offline

Impact:
With Ollama running, the app uses local embeddings and the local LLM. Without Ollama, it can still search existing NoteChunk rows locally and avoid external services.

---

## 2026-06-10

### Decision: Store extracted PDF text in SQLite and chunks in a NoteChunk table before vector storage

Reason:
This keeps uploaded note text visible to the local Django app immediately and provides a simple database-backed source for later ChromaDB indexing.

Alternatives Considered:

- Store chunks only in ChromaDB
- Store extracted text only on disk

Impact:
The dashboard and note detail pages can work before the vector store is implemented, while T009-T011 can index existing NoteChunk rows later.

---

## Initial Decisions

### Decision: Use Django monolith for MVP

Reason:
The user is learning Django and wants a practical AI project. Django is suitable for authentication, file upload, templates, database models, and backend logic.

Alternatives Considered:

- FastAPI
- Flask
- React + API backend

Impact:
Simpler MVP and easier learning path.

---

### Decision: App must be local-only

Reason:
Student notes may contain private study material. The user explicitly requested no API calls or cloud AI services.

Alternatives Considered:

- OpenAI API
- Gemini API
- Cloud vector DB

Impact:
Use local LLM, local embeddings, and local vector store.

---

### Decision: Use Ollama for local LLM

Reason:
Ollama is beginner-friendly and exposes a local localhost interface.

Alternatives Considered:

- llama.cpp directly
- GPT4All
- LM Studio

Impact:
Django can call the local model using localhost requests.

---

### Decision: Use ChromaDB for MVP vector store

Reason:
ChromaDB is simple for local RAG and stores vectors locally.

Alternatives Considered:

- FAISS
- pgvector

Impact:
Faster MVP implementation.

---

### Decision: Start with PDF only

Reason:
PDF notes are the most common student input format. Adding DOCX, PPT, and OCR increases complexity.

Alternatives Considered:

- DOCX upload
- PPT upload
- Image OCR

Impact:
MVP remains focused and achievable.
