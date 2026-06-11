# Local Setup Guide — AI Study Buddy

## 1. Create Project Folder

```powershell
mkdir ai_study_buddy
cd ai_study_buddy
```

## 2. Create Virtual Environment

```powershell
python -m venv venv
```

## 3. Activate Virtual Environment

PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Command Prompt:

```cmd
venv\Scripts\activate.bat
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
venv\Scripts\Activate.ps1
```

## 4. Install Dependencies

```powershell
pip install django pymupdf chromadb requests xhtml2pdf python-dotenv python-docx python-pptx Pillow pytesseract "psycopg[binary]"
```

## 5. Freeze Requirements

```powershell
pip freeze > requirements.txt
```

## 6. Create Django Project

```powershell
django-admin startproject config .
```

## 7. Create Django Apps

```powershell
python manage.py startapp accounts
python manage.py startapp dashboard
python manage.py startapp notes
python manage.py startapp rag
python manage.py startapp quiz
python manage.py startapp flashcards
python manage.py startapp summaries
```

## 8. Run Migrations

```powershell
python manage.py migrate
```

## 9. Run Server

```powershell
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## 10. Install Ollama

Install Ollama manually from its official installer.

After installation, pull local models:

```powershell
ollama pull gemma3:1b
ollama pull nomic-embed-text
```

Test chat model:

```powershell
ollama run gemma3:1b
```

## 11. Install Tesseract OCR

Image note OCR uses `pytesseract`, which requires the Tesseract executable to be installed separately and available on PATH.

On Windows, install Tesseract OCR and restart the terminal before uploading image notes.

## 12. Optional PostgreSQL

SQLite remains the default. To use PostgreSQL:

1. Copy `.env.example` to `.env`.
2. Set `DB_ENGINE=postgresql`.
3. Set the `POSTGRES_*` values.
4. Create the configured database.
5. Run:

```powershell
python manage.py migrate
```

Use `DB_ENGINE=sqlite` to return to local SQLite.

## 13. Local-Only Reminder

Localhost calls to Ollama are acceptable:

```text
http://localhost:11434
```

Do not call external AI APIs.
