from fastapi.testclient import TestClient

from app.main import app


def test_healthcheck() -> None:
    client = TestClient(app)
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_without_api_prefix_is_not_available() -> None:
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 404
