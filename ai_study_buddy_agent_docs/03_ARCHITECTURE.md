# Architecture — AI Study Buddy

## 1. Architecture Style

The MVP uses a simple Django monolith with local AI services.

```text
Browser
  ↓
Django Views / Templates
  ↓
Django Apps
  ↓
SQLite Database
  ↓
Local RAG Engine
  ↓
Local Vector Store
  ↓
Ollama Local LLM
```

## 2. Django Apps

Recommended apps:

```text
accounts/
dashboard/
notes/
rag/
quiz/
flashcards/
summaries/
```

## 3. Main Components

### 3.1 Accounts App

Handles:

- Register
- Login
- Logout
- User ownership

### 3.2 Dashboard App

Shows:

- Total notes
- Recent notes
- Total quizzes
- Total flashcards
- Total summaries
- Quick action buttons

### 3.3 Notes App

Handles:

- PDF upload
- File storage
- Text extraction
- Note metadata
- Note chunk creation

### 3.4 RAG App

Handles:

- Chunking
- Embeddings
- Vector storage
- Similarity search
- Local LLM response generation

### 3.5 Quiz App

Handles:

- Quiz generation
- Quiz saving
- Quiz result page
- PDF export

### 3.6 Flashcards App

Handles:

- Flashcard generation
- Flashcard list
- CSV export

### 3.7 Summaries App

Handles:

- Bullet summaries
- Paragraph summaries
- Exam-focused summaries

## 4. Local AI Runtime

Use Ollama running locally:

```text
Django → localhost Ollama → Local model response
```

This is allowed because localhost communication does not send notes to the cloud.

## 5. Data Flow

```text
Upload PDF
  ↓
Extract text
  ↓
Split into chunks
  ↓
Generate embeddings
  ↓
Store chunks and vectors
  ↓
Ask question / generate quiz / flashcards / summary
  ↓
Retrieve relevant chunks
  ↓
Generate response locally
```

## 6. Storage

### SQLite

Stores:

- Users
- Notes
- Extracted text metadata
- Quiz records
- Flashcards
- Summaries
- Chat history

### Vector Store

Stores:

- Chunk text
- Chunk metadata
- Embeddings

Recommended for MVP:

- ChromaDB

Alternative:

- FAISS

## 7. Security and Privacy

- Notes are stored locally.
- AI processing is local.
- Do not log full student notes unnecessarily.
- Restrict each user's access to their own notes.
- Validate uploaded file type.
- Limit upload size.

## 8. Suggested Folder Structure

```text
ai_study_buddy/
│
├── manage.py
├── requirements.txt
├── db.sqlite3
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/
├── dashboard/
├── notes/
├── rag/
├── quiz/
├── flashcards/
├── summaries/
│
├── rag_engine/
│   ├── pdf_reader.py
│   ├── text_splitter.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── llm_client.py
│   ├── answer_generator.py
│   ├── quiz_generator.py
│   ├── flashcard_generator.py
│   └── summary_generator.py
│
├── templates/
├── static/
├── media/
└── chroma_db/
```
