"""Safe readiness behavior for invalid database configuration."""

from fastapi.testclient import TestClient

from backend.app.main import app


def test_missing_database_configuration_is_safe(monkeypatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.chdir("/tmp")

    response = TestClient(app).get("/ready")

    assert response.status_code == 503
    assert response.json() == {
        "status": "not_ready",
        "code": "database_unavailable",
    }
    assert "password" not in response.text.lower()


def test_invalid_database_configuration_is_safe(monkeypatch) -> None:
    secret = "never-print-this-password"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{secret}")

    response = TestClient(app).get("/ready")

    assert response.status_code == 503
    assert response.json() == {
        "status": "not_ready",
        "code": "database_unavailable",
    }
    assert secret not in response.text
