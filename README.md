# JobFlow

A personal job-search assistant that discovers relevant jobs, sends alerts,
and manages user-approved applications. The current backend has FastAPI process
health plus a PostgreSQL schema managed by Alembic.

## Requirements

- Python 3.11 or newer
- Docker Desktop

## Run locally

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
cp .env.example .env
docker compose up -d --wait postgres
alembic upgrade head
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

The process-health endpoint does not touch dependencies. Database readiness is
reported separately:

```bash
curl --fail http://127.0.0.1:8000/ready
```

Expected response when PostgreSQL is available:

```json
{"status":"ready"}
```

If configuration is missing or PostgreSQL cannot be reached, `/ready` returns
HTTP 503 with the stable code `database_unavailable`; credentials are not
included in the response.

Interactive API documentation is available at <http://127.0.0.1:8000/docs>.

Stop the development server with `Ctrl+C`.

## Database workflow

The Compose service runs PostgreSQL 18.6 and stores development data in the
named `jobflow_postgres_data` volume. `docker compose stop` and container
restarts preserve that volume. Do not use `docker compose down --volumes`
unless you intentionally want to delete local database data.

The initial schema contains:

- `jobs`: a listing with a UUID, descriptive fields, optional source identity,
  and a unique `(source, external_job_id)` pair;
- `profiles`: verified owner facts;
- `preferences`: a one-to-one child of a profile with initial discovery rules.

Every table has a server-compatible UUID primary key plus timezone-aware
`created_at` and `updated_at` columns. SQLAlchemy updates `updated_at` when an
ORM update is issued. Later tickets can add database-side triggers if writes
outside SQLAlchemy become a real requirement.

Apply pending migrations:

```bash
alembic upgrade head
```

Run all tests against the isolated Docker test database:

```bash
TEST_DATABASE_URL=postgresql+psycopg://jobflow:jobflow@localhost:5432/jobflow_test \
  pytest -q
```

Stop PostgreSQL when finished:

```bash
docker compose stop
```

## Project structure

```text
backend/
  app/
    config.py     # Validated environment settings
    db/           # SQLAlchemy models and session construction
    main.py       # FastAPI health and readiness routes
docker/
  postgres/       # Local test-database initialization
migrations/       # Reviewed Alembic schema history
tests/            # Readiness and PostgreSQL integration tests
docs/
  learning-log.md # Session notes and validation evidence
  progress.md     # Current ticket status and next action
```
