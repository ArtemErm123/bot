import pytest

from backend.services.compare import compare_mix_variants


def test_compare_mix_variants_success() -> None:
    left = {"strength_mpa": 42.0, "lcc": 215000.0, "predicted_service_life_years": 42.0}
    right = {"strength_mpa": 38.5, "lcc": 225000.0, "predicted_service_life_years": 39.0}

    result = compare_mix_variants(left, right)

    assert result["strength_mpa"] == "left"
    assert result["lcc"] == "left"
    assert result["predicted_service_life_years"] == "left"
    assert result["overall"] == "left"


def test_compare_mix_variants_missing_metric() -> None:
    left = {"strength_mpa": 42.0, "lcc": 215000.0}
    right = {"strength_mpa": 38.5, "lcc": 225000.0, "predicted_service_life_years": 39.0}

    with pytest.raises(ValueError):
        compare_mix_variants(left, right)
