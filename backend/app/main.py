"""JobFlow API entry point."""

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from backend.app.db.session import create_database_engine


app = FastAPI(title="JobFlow")


@app.get("/health")
async def health() -> dict[str, str]:
    """Report that the API process is running."""
    return {"status": "ok"}


@app.get("/ready", response_model=None)
def readiness() -> JSONResponse:
    """Report whether the configured PostgreSQL database accepts queries."""

    try:
        engine = create_database_engine()
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        engine.dispose()
    except (ValidationError, SQLAlchemyError):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not_ready", "code": "database_unavailable"},
        )
    return JSONResponse(content={"status": "ready"})
