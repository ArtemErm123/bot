from dataclasses import dataclass


@dataclass(frozen=True)
class ConstructionInput:
    length_m: float
    width_m: float
    height_m: float


def calculate_structure_volume(data: ConstructionInput) -> float:
    """Return construction volume in cubic meters."""
    if min(data.length_m, data.width_m, data.height_m) <= 0:
        raise ValueError("All dimensions must be positive")
    return round(data.length_m * data.width_m * data.height_m, 4)
