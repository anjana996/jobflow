"""FastAPI dependencies shared by HTTP routes."""

from collections.abc import Iterator
from functools import lru_cache

from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from backend.app.db.session import create_database_engine, create_session_factory


@lru_cache
def get_database_engine() -> Engine:
    """Create one connection pool for the lifetime of the API process."""

    return create_database_engine()


@lru_cache
def get_session_factory() -> sessionmaker[Session]:
    """Create one reusable factory for short-lived request sessions."""

    return create_session_factory(get_database_engine())


def get_db_session() -> Iterator[Session]:
    """Provide one session for a request and always close it afterward."""

    with get_session_factory()() as session:
        yield session
