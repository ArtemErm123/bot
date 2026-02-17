from app.schemas.calculations import LifetimePredictionRequest, LifetimePredictionResponse


def predict_lifetime(payload: LifetimePredictionRequest) -> LifetimePredictionResponse:
    years = (payload.cover_mm / payload.chloride_exposure_factor) * 1.2
    return LifetimePredictionResponse(predicted_years=round(years, 2))
