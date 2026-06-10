# AI Study Buddy — Agent Documentation Index

This folder exists so the AI coding agent does not need to read the entire project every time.

Before making any code changes, the agent must read these files in order:

1. `16_AGENT_RULES.md`
2. `07_TASK_BOARD.md`
3. `08_PROGRESS_LOG.md`
4. `09_DECISION_LOG.md`
5. `02_PRD.md`
6. `03_ARCHITECTURE.md`
7. `13_RAG_PIPELINE.md`

## Project Summary

AI Study Buddy is a local-only Django web application where students upload notes and use AI features without cloud API calls.

Core MVP features:

- Student login/register
- Student dashboard
- Upload PDF notes
- Extract text from PDF notes
- Local RAG chatbot
- Auto quiz generator
- Export quiz as PDF
- Flashcard generator
- Export flashcards as CSV
- Summary generator

## Local-Only Requirement

The app must work locally on the user's system.

Do not use:

- OpenAI API
- Gemini API
- Claude API
- Pinecone
- Cloud vector databases
- External hosted AI services

Allowed local tools:

- Django
- SQLite
- Ollama running on localhost
- ChromaDB or FAISS
- Local embedding model
- Local PDF/text processing libraries

## Agent Workflow

For every development session:

1. Read `07_TASK_BOARD.md`.
2. Pick the next pending task.
3. Update task status from `Pending` to `In Progress`.
4. Implement the change.
5. Test the change.
6. Update task status to `Finished`.
7. Add a short entry in `08_PROGRESS_LOG.md`.
8. Add technical decisions in `09_DECISION_LOG.md` if any.
9. Update `10_CHANGELOG.md` if user-facing behavior changed.

## Status Terms

Use only these status values:

- Pending
- In Progress
- Blocked
- Finished

## Important

Never rewrite these files completely unless required. Append updates to logs and update only the relevant task rows.
