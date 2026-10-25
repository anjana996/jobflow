"""JF-7 PostgreSQL migration and transaction scenarios."""

from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, inspect, select
from sqlalchemy.orm import Session

from backend.app.db.models import Job


def test_migration_creates_expected_tables_and_constraints(
    empty_database: Engine,
) -> None:
    command.upgrade(Config("alembic.ini"), "head")
    inspector = inspect(empty_database)

    assert {"alembic_version", "jobs", "profiles", "preferences"} <= set(
        inspector.get_table_names()
    )
    assert {constraint["name"] for constraint in inspector.get_unique_constraints("jobs")} == {
        "uq_jobs_source_external_id"
    }
    assert {constraint["name"] for constraint in inspector.get_unique_constraints("preferences")} == {
        "uq_preferences_profile_id"
    }


def test_job_survives_new_session(migrated_engine: Engine) -> None:
    job_id = uuid4()
    with Session(migrated_engine) as session:
        session.add(Job(id=job_id, title="Backend Engineer", company="Example GmbH"))
        session.commit()

    with Session(migrated_engine) as new_session:
        stored = new_session.get(Job, job_id)

    assert stored is not None
    assert stored.title == "Backend Engineer"
    assert stored.company == "Example GmbH"
    assert stored.created_at is not None
    assert stored.updated_at is not None


def test_error_rolls_back_entire_transaction(migrated_engine: Engine) -> None:
    first_id = uuid4()
    with pytest.raises(RuntimeError, match="synthetic failure"):
        with Session(migrated_engine) as session, session.begin():
            session.add(Job(id=first_id, title="First", company="Example GmbH"))
            session.flush()
            raise RuntimeError("synthetic failure")

    with Session(migrated_engine) as session:
        assert session.scalar(select(Job).where(Job.id == first_id)) is None
