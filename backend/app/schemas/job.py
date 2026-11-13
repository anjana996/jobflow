"""Validation contracts for the Job API."""

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, HttpUrl, StringConstraints


RequiredText = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
]


class JobCreate(BaseModel):
    """Fields accepted when a client saves a job."""

    title: RequiredText
    company: RequiredText
    location: str | None = None
    description: str | None = None
    canonical_url: HttpUrl | None = None
    source: str | None = None
    external_job_id: str | None = None


class JobRead(JobCreate):
    """A persisted job returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime


class JobList(BaseModel):
    """A collection response with an explicit result count."""

    items: list[JobRead]
    count: int
