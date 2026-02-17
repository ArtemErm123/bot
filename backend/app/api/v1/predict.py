from fastapi import APIRouter

from app.schemas.calculations import LifetimePredictionRequest, LifetimePredictionResponse
from app.services.lifetime import predict_lifetime

router = APIRouter(prefix="/predict", tags=["predict"])


@router.post("/lifetime", response_model=LifetimePredictionResponse)
def lifetime(payload: LifetimePredictionRequest) -> LifetimePredictionResponse:
    return predict_lifetime(payload)
