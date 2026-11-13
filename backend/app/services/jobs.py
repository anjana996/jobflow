"""Database operations for saved jobs."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.models import Job
from backend.app.schemas.job import JobCreate


def create_job(session: Session, payload: JobCreate) -> Job:
    """Persist a validated job and return its database-generated values."""

    job = Job(**payload.model_dump(mode="json"))
    session.add(job)
    session.commit()
    session.refresh(job)
    return job


def get_job(session: Session, job_id: UUID) -> Job | None:
    """Return one saved job, or None when the ID does not exist."""

    return session.get(Job, job_id)


def list_jobs(session: Session) -> list[Job]:
    """Return all saved jobs in deterministic creation order."""

    statement = select(Job).order_by(Job.created_at, Job.id)
    return list(session.scalars(statement))
