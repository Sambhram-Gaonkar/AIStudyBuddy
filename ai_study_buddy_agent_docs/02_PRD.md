# Product Requirements Document — AI Study Buddy

## 1. Product Name

AI Study Buddy

## 2. One-Line Description

A local-only AI learning assistant that lets students upload notes and generate grounded answers, quizzes, flashcards, and summaries from their own study material.

## 3. Target Users

- School students
- College students
- Self-learners
- Exam preparation students

## 4. Problem Statement

Students have large notes, PDFs, and study material. Reading everything repeatedly is time-consuming. They need a tool that can help them understand, revise, and practice from their own notes.

## 5. Solution

Build a local AI study assistant that processes uploaded notes and provides:

- Note-based question answering
- Quiz generation
- Flashcard generation
- Summary generation
- Dashboard for activity tracking

## 6. Local-Only Privacy Requirement

Student notes must remain on the user's machine.

The application must not send uploaded notes or extracted text to external APIs.

## 7. MVP Features

### 7.1 Student Authentication

Students can:

- Register
- Login
- Logout
- Access only their own notes and generated content

### 7.2 Student Dashboard

Dashboard must show:

- Total uploaded notes
- Recent uploaded notes
- Total quizzes generated
- Total flashcards generated
- Total summaries generated
- Quick actions:
  - Upload Notes
  - Ask AI
  - Generate Quiz
  - Generate Flashcards
  - Generate Summary

### 7.3 Upload PDF Notes

Students can upload PDF notes.

System must:

- Save the PDF
- Extract text
- Store note metadata
- Split extracted text into chunks
- Store chunks for retrieval

### 7.4 RAG Chatbot

Students can ask questions from uploaded notes.

System must:

- Retrieve relevant chunks
- Send chunks to local LLM
- Generate answer based only on notes
- Say when answer is not found in notes

Required fallback:

> I could not find this in your uploaded notes.

### 7.5 Auto Quiz Generator

Students can generate:

- MCQs
- True/False questions
- Short answer questions

Options:

- Number of questions
- Difficulty
- Question type

### 7.6 Export Quiz as PDF

Generated quiz can be downloaded as a PDF.

PDF must include:

- Quiz title
- Note name
- Date generated
- Questions
- Options
- Correct answers
- Explanations

### 7.7 Flashcard Generator

System generates key term and definition cards from notes.

Each flashcard includes:

- Front text
- Back text
- Related note

### 7.8 Export Flashcards as CSV

CSV format:

```csv
Term,Definition
Newton's Third Law,Every action has an equal and opposite reaction.
```

### 7.9 Summary Generator

Students can generate:

- Bullet summary
- Paragraph summary
- Exam-focused summary
- Beginner-friendly summary

## 8. Out of Scope for MVP

Do not build these in MVP:

- Mobile app
- React frontend
- Payment system
- Multi-school admin panel
- Cloud deployment
- Collaborative classroom features
- Voice input
- Handwritten OCR
- PPT/DOCX upload

## 9. Success Criteria

MVP is successful when:

- A student can upload a PDF
- The app extracts text correctly
- The chatbot answers from uploaded notes
- Quiz generation works
- Quiz can be exported as PDF
- Flashcards are generated
- Flashcards can be exported as CSV
- Summary generation works
- Dashboard shows basic counts and recent activity
