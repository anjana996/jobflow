"""Database engine and session construction."""

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.app.config import get_settings


def create_database_engine(database_url: str | None = None) -> Engine:
    """Create an engine without logging the credential-bearing URL."""

    url = database_url or get_settings().database_url.get_secret_value()
    return create_engine(url, pool_pre_ping=True)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Build short-lived transactional sessions bound to an engine."""

    return sessionmaker(bind=engine, expire_on_commit=False)
