# Testing Plan — AI Study Buddy

## 1. Authentication Testing

Test cases:

- User can register
- User can login
- User can logout
- Invalid login shows error
- User cannot access another user's notes

## 2. Dashboard Testing

Test cases:

- Dashboard loads after login
- Correct note count is displayed
- Correct quiz count is displayed
- Correct flashcard count is displayed
- Recent notes are shown

## 3. PDF Upload Testing

Test cases:

- Valid PDF uploads successfully
- Non-PDF file is rejected
- Empty file is rejected
- Uploaded file is saved
- Note record is created

## 4. Text Extraction Testing

Test cases:

- Text is extracted from readable PDF
- Empty extraction shows helpful error
- Page numbers are captured if possible

## 5. RAG Testing

Test cases:

- Question retrieves relevant chunks
- Answer is generated from notes
- Unknown question returns fallback message
- User can only query own notes
- Questions, answers, and sources are saved
- User can only view own chat history

## 6. Quiz Testing

Test cases:

- MCQ quiz is generated
- True/False quiz is generated
- Short answer quiz is generated
- Quiz is saved in database
- Quiz result page displays correctly

## 7. Quiz PDF Export Testing

Test cases:

- PDF download works
- PDF includes note title
- PDF includes questions
- PDF includes answers
- PDF includes explanations

## 8. Flashcard Testing

Test cases:

- Flashcards are generated
- Flashcards are saved
- Flashcards display correctly
- CSV export works
- CSV contains term and definition

## 9. Summary Testing

Test cases:

- Bullet summary is generated
- Paragraph summary is generated
- Exam-focused summary is generated
- Summary is saved

## 10. Local-Only Testing

Test cases:

- App works without OpenAI/Gemini API keys
- App does not require cloud vector DB
- App uses local Ollama endpoint only
- Uploaded notes are not sent to external services
