# Deployment Guide - AI Study Buddy

This app is local-first. Keep uploaded notes, database files, ChromaDB data, Ollama, and OCR processing on the machine you control.

## 1. Prepare Environment

```powershell
git clone https://github.com/Sambhram-Gaonkar/AIStudyBuddy.git
cd AIStudyBuddy
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Generate a long random `DJANGO_SECRET_KEY` and place it in `.env`.

For local-only use:

```text
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DB_ENGINE=sqlite
```

## 2. Prepare Database and Static Files

```powershell
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy
```

`check --deploy` may warn about HTTPS settings. For localhost-only HTTP, keep secure-cookie and redirect settings disabled. Enable them only behind working HTTPS.

## 3. Start with Waitress

Loopback-only:

```powershell
waitress-serve --listen=127.0.0.1:8001 config.wsgi:application
```

Open:

```text
http://127.0.0.1:8001/
```

## 4. Optional Local Network Access

To allow trusted devices on the same LAN:

```text
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.1.20
```

Then bind Waitress:

```powershell
waitress-serve --listen=0.0.0.0:8001 config.wsgi:application
```

Replace `192.168.1.20` with the server machine's LAN IP. Restrict firewall access to trusted local networks. Do not expose this port directly to the public internet.

## 5. Optional PostgreSQL

Set:

```text
DB_ENGINE=postgresql
POSTGRES_DB=ai_study_buddy
POSTGRES_USER=postgres
POSTGRES_PASSWORD=change-me
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Create the database, then run:

```powershell
python manage.py migrate
```

## 6. Local Services

Ollama:

```powershell
ollama serve
ollama pull gemma3:1b
ollama pull nomic-embed-text
```

Image OCR requires Tesseract OCR installed on the same machine.

## 7. Backups

Back up:

- `db.sqlite3` when using SQLite
- PostgreSQL database dumps when using PostgreSQL
- `media/`
- `chroma_db/`
- `.env` in a secure location

Never commit `.env`, uploaded notes, local databases, or ChromaDB files.

## 8. HTTPS

For any non-local or internet-facing deployment:

- Put a reverse proxy with HTTPS in front of Waitress.
- Set `DJANGO_DEBUG=false`.
- Set exact `DJANGO_ALLOWED_HOSTS`.
- Set `DJANGO_CSRF_TRUSTED_ORIGINS=https://your-domain`.
- Enable secure cookies and HTTPS redirect.
- Run `python manage.py check --deploy`.

Do not expose student notes or Ollama endpoints publicly.
