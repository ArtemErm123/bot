from fastapi import APIRouter

from app.schemas.calculations import (
    MixPropertiesRequest,
    MixPropertiesResponse,
    StructureCalcRequest,
    StructureCalcResponse,
)
from app.services.mix_properties import calculate_mix_properties
from app.services.structure import calculate_structure

router = APIRouter(prefix="/calculate", tags=["calculate"])


@router.post("/structure", response_model=StructureCalcResponse)
def structure(payload: StructureCalcRequest) -> StructureCalcResponse:
    return calculate_structure(payload)


@router.post("/mix-properties", response_model=MixPropertiesResponse)
def mix_properties(payload: MixPropertiesRequest) -> MixPropertiesResponse:
    return calculate_mix_properties(payload)
