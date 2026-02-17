from dataclasses import dataclass


@dataclass(frozen=True)
class MixInput:
    cement: float
    water: float
    aggregate: float


def predict_mixture_properties(data: MixInput) -> dict[str, float]:
    """Simple deterministic predictor for unit testing critical business logic."""
    total = data.cement + data.water + data.aggregate
    if min(data.cement, data.water, data.aggregate) < 0 or total <= 0:
        raise ValueError("Mix components must be non-negative and not all zero")

    water_cement_ratio = round(data.water / data.cement, 4) if data.cement else 0.0
    density = round(total / 1.0, 2)
    strength_mpa = round(max(5.0, 60 - water_cement_ratio * 35), 2)

    return {
        "water_cement_ratio": water_cement_ratio,
        "density": density,
        "strength_mpa": strength_mpa,
    }
