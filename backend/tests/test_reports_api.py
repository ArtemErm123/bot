from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_generate_and_get_status() -> None:
    response = client.post(
        "/reports/generate",
        json={"kind": "short", "format": "pdf", "payload": {"records": [{"id": 1}]}},
    )
    assert response.status_code == 200
    report_id = response.json()["report_id"]

    status_response = client.get(f"/reports/{report_id}")
    assert status_response.status_code == 200
    body = status_response.json()
    assert body["status"] in {"pending", "in_progress", "completed"}


def test_not_found_report() -> None:
    response = client.get("/reports/missing-id")
    assert response.status_code == 404


def test_openapi_contract_prefixes_are_exposed() -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200

    paths = response.json()["paths"]
    assert "/api/health" in paths
    assert "/api/v1/reports" in paths
    assert "/reports/generate" in paths
