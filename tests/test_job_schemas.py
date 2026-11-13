"""Focused tests for the Job API validation contract."""

import pytest
from pydantic import ValidationError

from backend.app.schemas.job import JobCreate


def test_job_create_accepts_required_fields_and_trims_whitespace() -> None:
    job = JobCreate(title="  Backend Engineer  ", company=" Example GmbH ")

    assert job.title == "Backend Engineer"
    assert job.company == "Example GmbH"
    assert job.location is None


def test_job_create_requires_title() -> None:
    with pytest.raises(ValidationError) as error:
        JobCreate(company="Example GmbH")  # type: ignore[call-arg]

    assert error.value.errors()[0]["loc"] == ("title",)


def test_job_create_rejects_blank_required_text_and_invalid_url() -> None:
    with pytest.raises(ValidationError) as error:
        JobCreate(
            title="   ",
            company="Example GmbH",
            canonical_url="not-a-url",  # type: ignore[arg-type]
        )

    invalid_fields = {item["loc"] for item in error.value.errors()}
    assert invalid_fields == {("title",), ("canonical_url",)}
