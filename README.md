# JobFlow

A personal job-search assistant that discovers relevant jobs, sends alerts,
and manages user-approved applications. JF-5 provides the initial FastAPI
backend and its process-health endpoint.

## Requirements

- Python 3.10 or newer

## Run locally

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn backend.app.main:app --reload
```

The API is available at <http://127.0.0.1:8000>. Check its health with:

```bash
curl --fail http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

Interactive API documentation is available at <http://127.0.0.1:8000/docs>.

Stop the development server with `Ctrl+C`.

## Project structure

```text
backend/
  app/
    main.py       # FastAPI application and health route
docs/
  learning-log.md # Session notes and validation evidence
  progress.md     # Current ticket status and next action
```
