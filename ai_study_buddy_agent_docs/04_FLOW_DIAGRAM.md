# Flow Diagrams — AI Study Buddy

## 1. Overall System Flow

```mermaid
flowchart TD
    A[Student Login] --> B[Student Dashboard]
    B --> C[Upload PDF Notes]
    C --> D[Extract Text Locally]
    D --> E[Split Text into Chunks]
    E --> F[Generate Local Embeddings]
    F --> G[Store in Local Vector DB]
    G --> H{Choose Feature}
    H --> I[RAG Chatbot]
    H --> J[Quiz Generator]
    H --> K[Flashcard Generator]
    H --> L[Summary Generator]
    J --> M[Export Quiz as PDF]
    K --> N[Export Flashcards as CSV]
```

## 2. RAG Chatbot Flow

```mermaid
flowchart TD
    A[Student Asks Question] --> B[Create Query Embedding]
    B --> C[Search Similar Chunks]
    C --> D[Retrieve Top Matching Chunks]
    D --> E[Build Prompt with Context]
    E --> F[Send to Local LLM]
    F --> G[Generate Answer]
    G --> H[Show Answer with Source]
```

## 3. PDF Upload and Indexing Flow

```mermaid
flowchart TD
    A[Upload PDF] --> B[Validate File]
    B --> C[Save File Locally]
    C --> D[Extract Text Using PyMuPDF]
    D --> E[Clean Extracted Text]
    E --> F[Split into Chunks]
    F --> G[Generate Embeddings]
    G --> H[Store Chunks in Vector DB]
    H --> I[Mark Note as Indexed]
```

## 4. Quiz Generation Flow

```mermaid
flowchart TD
    A[Select Note] --> B[Choose Quiz Options]
    B --> C[Retrieve Relevant Note Chunks]
    C --> D[Build Quiz Prompt]
    D --> E[Local LLM Generates Quiz]
    E --> F[Parse Questions]
    F --> G[Save Quiz]
    G --> H[Show Quiz Result]
    H --> I[Export as PDF]
```

## 5. Flashcard Generation Flow

```mermaid
flowchart TD
    A[Select Note] --> B[Retrieve Important Chunks]
    B --> C[Build Flashcard Prompt]
    C --> D[Local LLM Generates Cards]
    D --> E[Save Flashcards]
    E --> F[Show Flashcard List]
    F --> G[Export CSV]
```

## 6. Summary Generation Flow

```mermaid
flowchart TD
    A[Select Note] --> B[Choose Summary Type]
    B --> C[Retrieve Note Chunks]
    C --> D[Build Summary Prompt]
    D --> E[Local LLM Generates Summary]
    E --> F[Save Summary]
    F --> G[Display Summary]
```
