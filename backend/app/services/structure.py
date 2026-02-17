from app.schemas.calculations import StructureCalcRequest, StructureCalcResponse


def calculate_structure(payload: StructureCalcRequest) -> StructureCalcResponse:
    # Simply supported beam: Mmax = qL²/8
    moment = payload.load_kn_m * payload.span_m**2 / 8
    return StructureCalcResponse(moment_kn_m=round(moment, 3))
