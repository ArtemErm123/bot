from fastapi import APIRouter

from app.services.health_service import get_health

router = APIRouter(tags=["health"])


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return get_health()
