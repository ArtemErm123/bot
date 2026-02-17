import pytest

from backend.services.design_calculation import ConstructionInput, calculate_structure_volume


def test_calculate_structure_volume_success() -> None:
    data = ConstructionInput(length_m=10.0, width_m=3.5, height_m=0.2)
    assert calculate_structure_volume(data) == 7.0


def test_calculate_structure_volume_invalid_dimensions() -> None:
    data = ConstructionInput(length_m=10.0, width_m=0, height_m=0.2)
    with pytest.raises(ValueError):
        calculate_structure_volume(data)
