# Changelog — AI Study Buddy

Track user-facing changes here.

## Unreleased

### Added

- Django project scaffold with base configuration
- MVP Django app modules for accounts, dashboard, notes, rag, quiz, flashcards, and summaries
- Basic dashboard homepage at the root URL
- Student registration, login, and logout pages
- Authenticated student dashboard with counts, recent notes, and quick actions
- PDF note upload, local text extraction, and note chunking
- Local RAG chatbot page with ChromaDB retrieval, Ollama integration, and not-found fallback
- User-owned Ask AI history with saved questions, answers, and source metadata
- Responsive Stitch-inspired academic interface with sidebar navigation, mobile bottom navigation, progress analytics, tutor chat, quiz cards, and revealable flashcards
- Quiz generation for MCQ, true/false, and short-answer questions with PDF export
- Flashcard generation with CSV export
- Bullet, paragraph, and exam-focused summary generation
- Dashboard recent activity sections for notes, quizzes, flashcards, and summaries
- Responsive local MVP styling
- DOCX note upload with local text extraction
- PPTX note upload with local text extraction
- OCR image note upload for PNG, JPG, TIFF, and BMP files
- Quiz taking, score tracking, result review, and retry flow
- Flashcard revision mode with review history and mastery percentage
- User-owned subject folders with note assignment and filtering
- Optional PostgreSQL configuration through local environment variables
- Windows deployment guide with Waitress, WhiteNoise, environment-based security settings, and local/LAN instructions
- Local virtual environment and requirements.txt
- Initial project documentation
- MVP feature scope
- Local-only architecture
- Task board
- Roadmap
- Agent rules
- End-to-end regression coverage for PDF upload, chat, quiz, exports, flashcards, and summaries

### Changed

- Dashboard now shows generated study activity, not only note activity
- Dashboard now calculates quiz average, topic performance, weak topics, and recent results from stored attempts
- Shared app navigation, forms, cards, lists, and study pages now use the supplied clean interface design system
- Study generators now list only successfully processed notes
- Offline quiz and flashcard generators now return the requested item count

### Fixed

- Empty, oversized, corrupt, encrypted, and textless uploads now fail with clear form errors
- Upload parser failures no longer produce server errors
