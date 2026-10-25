# Learning log

## 2026-10-25 — JF-5: FastAPI health endpoint

### Concept

An HTTP client sends a method and path, such as `GET /health`, to Uvicorn.
Uvicorn passes the request to the FastAPI application. FastAPI matches the
method and path to the decorated function, awaits it, and serializes the
returned dictionary as a JSON response.

### Design trade-off

The health route lives in `main.py` for this first runnable slice. That keeps
the scaffold easy to trace. As business routes arrive, routers will separate
HTTP concerns by feature; creating that structure now would add indirection
without serving JF-5.

### Validation evidence

- Environment: macOS, Python 3.14.8, FastAPI 0.162.0, Uvicorn 0.53.0.
- Installed the pinned dependencies into a fresh `.venv`.
- Started `backend.app.main:app` on temporary port 8015 because unrelated
  Python processes already occupied the documented default port 8000.
- `GET /health` returned HTTP 200 with `{"status":"ok"}`.
- `GET /not-a-route` returned HTTP 404 with `{"detail":"Not Found"}`.
- `git check-ignore` confirmed `.env`, `.venv`, CV, application, and upload
  paths are ignored. `.env.example` remains trackable.
- No dedicated automated test was added because JF-5 explicitly calls for
  manual scaffold smoke checks; later behavior-bearing routes will use pytest.

### Next action

Review the diff, configure Git author identity, commit and push the ticket
branch, then open a pull request and attach its evidence to JF-5.
