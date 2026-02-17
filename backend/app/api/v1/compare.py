from fastapi import APIRouter

from app.schemas.calculations import CompareRequest, CompareResponse
from app.services.compare import compare_variants

router = APIRouter(tags=["compare"])


@router.post("/compare", response_model=CompareResponse)
def compare(payload: CompareRequest) -> CompareResponse:
    return compare_variants(payload)
