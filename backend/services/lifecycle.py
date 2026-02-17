from dataclasses import dataclass


@dataclass(frozen=True)
class LifecycleInput:
    base_service_life_years: int
    environment_factor: float
    initial_cost: float
    annual_maintenance_cost: float


def predict_service_life_and_lcc(data: LifecycleInput) -> dict[str, float]:
    if data.base_service_life_years <= 0:
        raise ValueError("base_service_life_years must be positive")
    if data.environment_factor <= 0:
        raise ValueError("environment_factor must be positive")
    if min(data.initial_cost, data.annual_maintenance_cost) < 0:
        raise ValueError("cost values cannot be negative")

    predicted_life = max(1, round(data.base_service_life_years / data.environment_factor))
    lcc = round(data.initial_cost + data.annual_maintenance_cost * predicted_life, 2)

    return {
        "predicted_service_life_years": float(predicted_life),
        "lcc": lcc,
    }
