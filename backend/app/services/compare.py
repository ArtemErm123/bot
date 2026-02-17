from app.schemas.calculations import CompareRequest, CompareResponse


def compare_variants(payload: CompareRequest) -> CompareResponse:
    diff = payload.left_value - payload.right_value
    winner = "left" if diff > 0 else "right" if diff < 0 else "equal"
    return CompareResponse(difference=round(diff, 3), winner=winner)
