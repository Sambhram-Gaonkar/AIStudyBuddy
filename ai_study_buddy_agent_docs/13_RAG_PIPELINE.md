# RAG Pipeline — AI Study Buddy

## 1. Goal

Allow students to ask questions from their own uploaded notes and get answers grounded in those notes.

## 2. Pipeline Steps

```text
PDF Upload
  ↓
Text Extraction
  ↓
Text Cleaning
  ↓
Chunking
  ↓
Embedding
  ↓
Vector Storage
  ↓
Retrieval
  ↓
Prompt Building
  ↓
Local LLM Answer
```

## 3. Text Extraction

Use PyMuPDF.

Output should include:

- Text
- Page number if possible

## 4. Text Cleaning

Clean:

- Extra whitespace
- Broken line breaks
- Empty lines
- Repeated headers/footers if possible

## 5. Chunking

Suggested settings:

```text
Chunk size: 800 to 1200 characters
Overlap: 100 to 200 characters
```

Each chunk metadata:

```text
user_id
note_id
note_title
page_number
chunk_index
```

## 6. Embeddings

Recommended local embedding model:

```text
nomic-embed-text
```

Alternative:

```text
all-MiniLM-L6-v2
```

## 7. Vector Store

Recommended:

```text
ChromaDB
```

Collection strategy:

```text
One collection for all notes
Filter by user_id and note_id during retrieval
```

## 8. Retrieval

For a question:

1. Generate embedding for question
2. Search top 3 to 5 matching chunks
3. Filter by user and selected note
4. Send chunks to local LLM as context

## 9. RAG Answer Prompt

```text
You are an AI study assistant.

Answer the student's question using only the provided notes.

If the answer is not present in the notes, say:
"I could not find this in your uploaded notes."

Keep the answer clear, simple, and student-friendly.

Notes:
{context}

Question:
{question}

Answer:
```

## 10. Quiz Prompt

```text
You are an exam question generator.

Create {number_of_questions} {question_type} questions from the notes below.

Difficulty: {difficulty}

For each question, include:
- question
- options if MCQ
- correct answer
- short explanation

Use only the provided notes.

Notes:
{context}
```

## 11. Flashcard Prompt

```text
You are a flashcard generator.

Create key term and definition flashcards from the notes below.

Return each card in this format:
Front: ...
Back: ...

Use only the provided notes.

Notes:
{context}
```

## 12. Summary Prompt

```text
You are a study notes summarizer.

Create a {summary_type} summary from the notes below.

Use simple student-friendly language.

Notes:
{context}
```

## 13. Hallucination Control

The local LLM must be instructed to answer only from retrieved notes.

If context is weak or unrelated, return:

```text
I could not find this in your uploaded notes.
```

## 14. Source Display

Whenever possible, show:

```text
Source: Note Title, Page Number
```
