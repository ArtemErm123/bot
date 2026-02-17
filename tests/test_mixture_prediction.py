import pytest

from backend.services.mixture_prediction import MixInput, predict_mixture_properties


def test_predict_mixture_properties_success() -> None:
    result = predict_mixture_properties(MixInput(cement=400, water=180, aggregate=1200))

    assert result["water_cement_ratio"] == 0.45
    assert result["density"] == 1780.0
    assert result["strength_mpa"] == 44.25


def test_predict_mixture_properties_invalid_mix() -> None:
    with pytest.raises(ValueError):
        predict_mixture_properties(MixInput(cement=0, water=0, aggregate=0))
