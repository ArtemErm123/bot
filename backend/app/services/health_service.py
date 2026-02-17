from app.domain.health import HealthStatus


def get_health() -> dict[str, str]:
    status = HealthStatus(status="ok")
    return {"status": status.status}
