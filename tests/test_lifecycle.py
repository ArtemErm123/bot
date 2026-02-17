import pytest

from backend.services.lifecycle import LifecycleInput, predict_service_life_and_lcc


def test_predict_service_life_and_lcc_success() -> None:
    result = predict_service_life_and_lcc(
        LifecycleInput(
            base_service_life_years=50,
            environment_factor=1.25,
            initial_cost=120000,
            annual_maintenance_cost=2500,
        )
    )

    assert result["predicted_service_life_years"] == 40.0
    assert result["lcc"] == 220000.0


def test_predict_service_life_and_lcc_invalid_base_life() -> None:
    with pytest.raises(ValueError):
        predict_service_life_and_lcc(
            LifecycleInput(
                base_service_life_years=0,
                environment_factor=1.25,
                initial_cost=100000,
                annual_maintenance_cost=2000,
            )
        )
