"""Focused tests for request-scoped database-session cleanup."""

from backend.app import dependencies


class FakeSession:
    """Small context manager that records whether cleanup happened."""

    def __init__(self) -> None:
        self.closed = False

    def __enter__(self) -> "FakeSession":
        return self

    def __exit__(self, *args: object) -> None:
        self.closed = True


def test_db_session_is_closed_after_dependency_finishes(monkeypatch) -> None:
    fake_session = FakeSession()
    monkeypatch.setattr(
        dependencies,
        "get_session_factory",
        lambda: lambda: fake_session,
    )
    dependency = dependencies.get_db_session()

    yielded_session = next(dependency)
    assert yielded_session is fake_session
    assert fake_session.closed is False

    try:
        next(dependency)
    except StopIteration:
        pass

    assert fake_session.closed is True
