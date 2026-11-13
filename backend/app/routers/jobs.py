"""HTTP routes for saved jobs."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.dependencies import get_db_session
from backend.app.schemas.job import JobCreate, JobList, JobRead
from backend.app.services import jobs as job_service


router = APIRouter(prefix="/api/v1/jobs", tags=["jobs"])
DatabaseSession = Annotated[Session, Depends(get_db_session)]


@router.post("", response_model=JobRead, status_code=status.HTTP_201_CREATED)
def create_job(payload: JobCreate, session: DatabaseSession) -> JobRead:
    """Save a job listing; this does not create an application."""

    return JobRead.model_validate(job_service.create_job(session, payload))


@router.get("", response_model=JobList)
def list_jobs(session: DatabaseSession) -> JobList:
    """List saved jobs."""

    jobs = job_service.list_jobs(session)
    return JobList(
        items=[JobRead.model_validate(job) for job in jobs],
        count=len(jobs),
    )


@router.get("/{job_id}", response_model=JobRead)
def get_job(job_id: UUID, session: DatabaseSession) -> JobRead:
    """Fetch a saved job by its UUID."""

    job = job_service.get_job(session, job_id)
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "job_not_found", "message": "Job not found"},
        )
    return JobRead.model_validate(job)
