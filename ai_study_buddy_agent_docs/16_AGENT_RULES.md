# Agent Rules — AI Study Buddy

These rules must be followed by every AI coding agent working on this project.

## 1. Read First

Before coding, read these files:

1. `07_TASK_BOARD.md`
2. `08_PROGRESS_LOG.md`
3. `09_DECISION_LOG.md`
4. `02_PRD.md`
5. `03_ARCHITECTURE.md`

## 2. Update Tracking Files

After every meaningful change:

- Update task status in `07_TASK_BOARD.md`
- Add entry to `08_PROGRESS_LOG.md`
- Add decision to `09_DECISION_LOG.md` if a technical choice was made
- Update `10_CHANGELOG.md` if user-facing behavior changed

## 3. Task Status Rules

Use only:

- Pending
- In Progress
- Blocked
- Finished

Do not invent other statuses.

## 4. Local-Only AI Rule

Never add code that sends notes, chunks, questions, or summaries to external AI APIs.

Forbidden:

- OpenAI API
- Gemini API
- Claude API
- Pinecone
- Cloud OCR
- Hosted model APIs

Allowed:

- Ollama localhost
- Local embeddings
- Local ChromaDB
- Local FAISS
- Local PDF extraction

## 5. Keep MVP Simple

Do not add:

- React
- Payments
- Cloud deployment
- Admin analytics
- Mobile app
- Multi-tenant school management

until MVP is finished.

## 6. Coding Style

- Keep code readable.
- Use service files for business logic.
- Keep views simple.
- Add comments only where helpful.
- Avoid over-engineering.

## 7. Security Rules

- Validate uploaded file type.
- Restrict users to their own notes.
- Do not expose full file paths in UI.
- Do not log private note content unnecessarily.
- Use Django authentication decorators.

## 8. Testing Rule

After implementing a feature, test the basic flow manually and record testing in `08_PROGRESS_LOG.md`.

## 9. If Blocked

If blocked:

1. Mark task as `Blocked`.
2. Add reason in task notes.
3. Add entry in progress log.
4. Continue with another independent pending task if possible.

## 10. Do Not Lose Context

These files are the memory of the project. Keep them updated.
