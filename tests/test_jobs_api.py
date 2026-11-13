"""JF-8 API integration scenarios against isolated PostgreSQL."""

from collections.abc import Iterator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, func, inspect, select
from sqlalchemy.orm import Session

from backend.app.db.models import Job
from backend.app.dependencies import get_db_session
from backend.app.main import app


@pytest.fixture()
def client(migrated_engine: Engine) -> Iterator[TestClient]:
    def test_session() -> Iterator[Session]:
        with Session(migrated_engine) as session:
            yield session

    app.dependency_overrides[get_db_session] = test_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_create_then_fetch_job(client: TestClient) -> None:
    payload = {
        "title": "Backend Engineer",
        "company": "Example GmbH",
        "location": "Berlin",
        "canonical_url": "https://example.com/jobs/backend-engineer",
    }

    created = client.post("/api/v1/jobs", json=payload)

    assert created.status_code == 201
    created_body = created.json()
    assert created_body["title"] == payload["title"]
    assert created_body["company"] == payload["company"]
    assert created_body["id"]
    assert created_body["created_at"]

    fetched = client.get(f"/api/v1/jobs/{created_body['id']}")

    assert fetched.status_code == 200
    assert fetched.json() == created_body


def test_list_jobs_returns_saved_jobs(client: TestClient) -> None:
    client.post(
        "/api/v1/jobs",
        json={"title": "First", "company": "Example GmbH"},
    )
    client.post(
        "/api/v1/jobs",
        json={"title": "Second", "company": "Example AG"},
    )

    response = client.get("/api/v1/jobs")

    assert response.status_code == 200
    assert response.json()["count"] == 2
    assert [job["title"] for job in response.json()["items"]] == [
        "First",
        "Second",
    ]


def test_invalid_payload_returns_422_without_creating_job(
    client: TestClient, migrated_engine: Engine
) -> None:
    response = client.post(
        "/api/v1/jobs",
        json={"title": "   ", "company": "Example GmbH"},
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "title"]
    with Session(migrated_engine) as session:
        assert session.scalar(select(func.count()).select_from(Job)) == 0


def test_unknown_job_returns_safe_404(client: TestClient) -> None:
    response = client.get(f"/api/v1/jobs/{uuid4()}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": {"code": "job_not_found", "message": "Job not found"}
    }


def test_saving_job_does_not_create_application(
    client: TestClient, migrated_engine: Engine
) -> None:
    response = client.post(
        "/api/v1/jobs",
        json={"title": "Saved only", "company": "Example GmbH"},
    )

    assert response.status_code == 201
    assert "application" not in response.json()
    assert "applied" not in response.json()
    assert "applications" not in inspect(migrated_engine).get_table_names()
