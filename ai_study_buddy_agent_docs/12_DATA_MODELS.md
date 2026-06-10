# Data Models — AI Study Buddy

## 1. Note

Stores uploaded notes.

Fields:

```text
id
user
title
file
extracted_text
is_indexed
created_at
updated_at
```

## 2. NoteChunk

Optional if storing chunk metadata in Django.

Fields:

```text
id
note
user
chunk_text
chunk_index
page_number
vector_id
created_at
```

If using ChromaDB metadata only, this model may be skipped.

## 3. ChatHistory

Stores student Q&A history.

Fields:

```text
id
user
note
question
answer
source_chunks
created_at
```

## 4. Quiz

Stores generated quiz.

Fields:

```text
id
user
note
title
question_type
difficulty
created_at
```

## 5. QuizQuestion

Stores quiz questions.

Fields:

```text
id
quiz
question_text
option_a
option_b
option_c
option_d
correct_answer
explanation
question_type
```

For True/False, use:

```text
option_a = True
option_b = False
```

For short answer, options can be empty.

## 6. Flashcard

Stores generated flashcards.

Fields:

```text
id
user
note
front
back
created_at
```

## 7. Summary

Stores generated summaries.

Fields:

```text
id
user
note
summary_type
content
created_at
```

## 8. ActivityLog

Optional but useful for dashboard.

Fields:

```text
id
user
activity_type
description
created_at
```

Activity types:

```text
NOTE_UPLOADED
QUIZ_GENERATED
FLASHCARDS_GENERATED
SUMMARY_GENERATED
QUESTION_ASKED
```
