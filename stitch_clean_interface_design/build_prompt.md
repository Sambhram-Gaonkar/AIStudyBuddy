# AI Agent Build Prompt
## AI Study Buddy — Complete Project Build Prompt

> Use this prompt with Cursor AI, Claude Code, or any AI coding agent to scaffold and build the full project.

---

## MASTER BUILD PROMPT

Copy everything below this line and paste it into your AI coding agent:

---

```
You are an expert Python full-stack developer. Build a complete, production-ready web application called "AI Study Buddy" — an AI-powered study tool that helps students learn from their own notes.

## PROJECT OVERVIEW

AI Study Buddy allows students to:
1. Upload their lecture notes (PDF, DOCX, TXT)
2. Chat with an AI tutor grounded in their notes (RAG)
3. Auto-generate quizzes with scoring
4. Auto-generate flashcards (term → definition)
5. Auto-generate topic summaries
6. Track weak topics based on quiz performance

## TECH STACK

- **Frontend:** Streamlit 1.35+
- **Backend:** FastAPI 0.111+
- **LLM:** Anthropic Claude API (model: claude-sonnet-4-20250514)
- **RAG Engine:** LlamaIndex 0.10+
- **Vector Store:** ChromaDB (local persistent)
- **PDF Parsing:** PyMuPDF (fitz)
- **DOCX Parsing:** python-docx
- **Database:** SQLite with SQLAlchemy
- **Environment:** python-dotenv
- **Deployment target:** Streamlit Cloud + Render (free tier)

## FOLDER STRUCTURE

Create this exact structure:

ai-study-buddy/
├── frontend/
│   └── app.py                    # Streamlit UI
├── backend/
│   ├── main.py                   # FastAPI app + routes
│   ├── parser.py                 # File parsing logic
│   ├── rag_engine.py             # LlamaIndex RAG setup
│   ├── ai_prompts.py             # All Claude prompt templates
│   ├── database.py               # SQLAlchemy models + DB logic
│   └── schemas.py                # Pydantic request/response models
├── data/
│   └── chroma_db/                # ChromaDB persistent storage
├── tests/
│   ├── test_parser.py
│   ├── test_rag.py
│   └── test_api.py
├── .env.example
├── requirements.txt
├── README.md
└── docs/
    ├── PRD.md
    ├── ARCHITECTURE.md
    └── FLOW_DIAGRAMS.md

## DETAILED IMPLEMENTATION INSTRUCTIONS

### 1. backend/parser.py

Implement a `DocumentParser` class with:
- `parse(file_path: str) -> str` method
- Handles .pdf using PyMuPDF: extract text from all pages
- Handles .docx using python-docx: extract all paragraphs
- Handles .txt: read and return
- Raises `ValueError` for unsupported types
- Strips extra whitespace and empty lines from output

### 2. backend/rag_engine.py

Implement a `RAGEngine` class with:
- `__init__(self, collection_name: str)` — initializes ChromaDB client and LlamaIndex
- `index_document(self, text: str, doc_id: str)` — chunks text into 512 token chunks with 50 token overlap, generates embeddings, stores in ChromaDB
- `query(self, question: str, top_k: int = 3) -> list[str]` — embeds query, retrieves top_k similar chunks, returns list of chunk strings
- Use `sentence-transformers/all-MiniLM-L6-v2` as the embedding model (local, no API key needed)
- ChromaDB collection stored in `./data/chroma_db/`

### 3. backend/ai_prompts.py

Create a `Prompts` class with static methods returning prompt strings:

```python
@staticmethod
def chat_prompt(context: str, question: str) -> str:
    return f"""You are a helpful study tutor. Answer the student's question using ONLY the context below. 
If the answer is not in the context, say "I couldn't find that in your notes."

Context:
{context}

Question: {question}

Answer:"""

@staticmethod  
def quiz_prompt(text: str, num_questions: int, difficulty: str) -> str:
    return f"""Generate {num_questions} multiple choice questions from the following notes.
Difficulty: {difficulty}

Return ONLY a valid JSON array in this exact format (no other text):
[
  {{
    "question": "question text",
    "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
    "answer": "A",
    "explanation": "brief explanation"
  }}
]

Notes:
{text}"""

@staticmethod
def flashcard_prompt(text: str) -> str:
    return f"""Extract the most important key terms and their definitions from these notes.

Return ONLY a valid JSON array (no other text):
[
  {{
    "term": "key term",
    "definition": "clear, concise definition"
  }}
]

Notes:
{text}"""

@staticmethod
def summary_prompt(text: str, length: str) -> str:
    length_instruction = "3-5 bullet points" if length == "short" else "8-12 detailed bullet points"
    return f"""Summarize the following notes into {length_instruction}.
Each bullet point should capture a key concept.

Notes:
{text}

Summary:"""
```

### 4. backend/database.py

Implement SQLite database with SQLAlchemy:
- `Session` table: id (UUID), name (str), created_at (datetime)
- `QuizResult` table: id, session_id (FK), topic (str), score (float), total_questions (int), timestamp (datetime)
- Functions:
  - `create_session(name: str) -> str` — returns session_id
  - `save_quiz_result(session_id, topic, score, total) -> None`
  - `get_weak_topics(session_id: str) -> list[str]` — topics where avg score < 0.6
  - `get_all_scores(session_id: str) -> list[dict]`

### 5. backend/main.py

FastAPI app with these endpoints:

**POST /upload**
- Accepts: multipart form with `file` and `session_id`
- Saves file to temp directory
- Calls `DocumentParser.parse()`
- Calls `RAGEngine.index_document()`
- Returns: `{success: true, preview: first_500_chars}`

**POST /chat**
- Accepts: `{session_id, question}`
- Calls `RAGEngine.query()` to get context chunks
- Builds prompt with `Prompts.chat_prompt()`
- Calls Claude API
- Returns: `{answer: str}`

**POST /quiz**
- Accepts: `{session_id, topic, num_questions, difficulty}`
- Retrieves relevant chunks for topic
- Calls Claude API with `Prompts.quiz_prompt()`
- Parses JSON response
- Returns: `{questions: [...]}`

**POST /quiz/submit**
- Accepts: `{session_id, topic, score, total}`
- Saves to SQLite via `database.save_quiz_result()`
- Returns: `{saved: true, weak_topics: [...]}`

**POST /flashcards**
- Accepts: `{session_id, topic}`
- Retrieves chunks, calls Claude with `Prompts.flashcard_prompt()`
- Returns: `{flashcards: [{term, definition}]}`

**POST /summary**
- Accepts: `{session_id, topic, length}` where length is "short" or "detailed"
- Retrieves chunks, calls Claude with `Prompts.summary_prompt()`
- Returns: `{summary: str}`

**GET /scores/{session_id}**
- Returns all quiz scores and weak topics for a session

For all Claude API calls use:
```python
import anthropic
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1500,
    messages=[{"role": "user", "content": prompt}]
)
return response.content[0].text
```

### 6. frontend/app.py

Streamlit UI with a sidebar and 5 main pages:

**Sidebar:**
- Session name input + "New Session" button
- File uploader (PDF, DOCX, TXT) with upload button
- Show uploaded files list
- Show weak topics list (pulled from backend)

**Page 1: 💬 Chat Tutor**
- Chat-style interface using `st.chat_message`
- Input at bottom
- Shows loading spinner during API call
- Displays chat history from `st.session_state`

**Page 2: 📝 Quiz**
- Select topic (dropdown from uploaded files)
- Select number of questions (5, 10)
- Select difficulty (Easy, Medium, Hard)
- "Generate Quiz" button
- Render each question with radio buttons for options
- "Submit Quiz" button → show score + explanations
- Show score as progress bar

**Page 3: 🃏 Flashcards**
- Select topic
- "Generate Flashcards" button
- Show cards in a grid (2 columns)
- Each card: click to "flip" (toggle term ↔ definition using st.button)
- "Export as CSV" download button

**Page 4: 📄 Summary**
- Select topic
- Toggle: Short / Detailed
- "Generate Summary" button
- Render markdown output

**Page 5: 📊 Progress**
- Bar chart of quiz scores per topic (using st.bar_chart)
- List of weak topics highlighted in red
- Total quizzes taken counter

### 7. requirements.txt

```
streamlit==1.35.0
fastapi==0.111.0
uvicorn==0.30.0
anthropic==0.28.0
llama-index==0.10.0
llama-index-vector-stores-chroma==0.1.0
chromadb==0.5.0
sentence-transformers==3.0.0
pymupdf==1.24.0
python-docx==1.1.0
sqlalchemy==2.0.30
python-multipart==0.0.9
python-dotenv==1.0.0
httpx==0.27.0
pydantic==2.7.0
```

### 8. .env.example

```
ANTHROPIC_API_KEY=your_api_key_here
BACKEND_URL=http://localhost:8000
CHROMA_DB_PATH=./data/chroma_db
DATABASE_URL=sqlite:///./data/study_buddy.db
```

## IMPORTANT IMPLEMENTATION NOTES

1. **Error handling:** Every API endpoint must have try/except and return proper HTTP error responses. Every Claude API call must handle `anthropic.APIError`.

2. **JSON parsing safety:** When parsing Claude's JSON responses (quiz, flashcards), use:
   ```python
   import json, re
   text = response.strip()
   # Strip markdown code fences if present
   text = re.sub(r'^```json\s*|\s*```$', '', text, flags=re.MULTILINE)
   data = json.loads(text)
   ```

3. **Session state in Streamlit:** Use `st.session_state` for:
   - `chat_history: list`
   - `current_session_id: str`
   - `uploaded_files: list`
   - `current_quiz: list`

4. **CORS in FastAPI:** Add `CORSMiddleware` allowing all origins (for development).

5. **Loading states:** Every Streamlit button that calls the backend must use `st.spinner()`.

6. **File cleanup:** After parsing, delete temp uploaded files from disk.

## TESTS

Write pytest tests for:
- `test_parser.py`: test PDF, DOCX, TXT parsing with sample files; test unsupported format raises ValueError
- `test_rag.py`: test indexing and querying returns non-empty results
- `test_api.py`: use FastAPI TestClient to test /upload, /chat, /quiz endpoints with mock Claude responses

## README.md

Generate a comprehensive README with:
- Project description
- Architecture overview
- Setup instructions (clone, .env, pip install, run backend, run frontend)
- Feature list with screenshots section (placeholder)
- API endpoint reference
- Tech stack badges
- Future scope section

## FINAL CHECKLIST

After building, verify:
- [ ] All 5 Streamlit pages render without errors
- [ ] File upload works for PDF, DOCX, and TXT
- [ ] Chat returns grounded answers
- [ ] Quiz generates valid MCQs and scores correctly
- [ ] Flashcards flip on click
- [ ] Summary renders properly
- [ ] Progress page shows scores from SQLite
- [ ] No API keys hardcoded anywhere
- [ ] README has setup instructions
- [ ] requirements.txt is complete and pinned
```

---

## HOW TO USE THIS PROMPT

### With Cursor AI:
1. Open Cursor, start a new project folder `ai-study-buddy`
2. Open Cursor Chat (Cmd+L)
3. Paste the full prompt above
4. Cursor will scaffold all files — review each one as it generates
5. Run `pip install -r requirements.txt` in terminal
6. Add your `.env` file with real API key
7. Run backend: `uvicorn backend.main:app --reload`
8. Run frontend: `streamlit run frontend/app.py`

### With Claude Code:
1. `cd` into your project folder
2. Run `claude` to start Claude Code
3. Paste the prompt or use `/init` then paste
4. Claude Code will implement file by file

### Iterating After Initial Build:
Use these follow-up prompts for refinement:

**Fix quiz JSON parsing:**
> "The quiz endpoint sometimes fails because Claude returns JSON with extra text. Add robust JSON extraction that strips markdown fences and handles partial responses."

**Improve RAG accuracy:**
> "The chat answers are sometimes off-topic. Improve the RAG query to retrieve top-5 chunks instead of top-3, and add a relevance score filter that drops chunks below 0.5 cosine similarity."

**Add loading UX:**
> "Add a progress bar to the file upload flow in Streamlit that shows: Parsing → Chunking → Embedding → Done"
