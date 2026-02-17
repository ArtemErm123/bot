from app.schemas.calculations import MixPropertiesRequest, MixPropertiesResponse


def calculate_mix_properties(payload: MixPropertiesRequest) -> MixPropertiesResponse:
    return MixPropertiesResponse(water_cement_ratio=round(payload.water_kg_m3 / payload.cement_kg_m3, 3))
