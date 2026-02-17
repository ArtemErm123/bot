def compare_mix_variants(left: dict[str, float], right: dict[str, float]) -> dict[str, str]:
    """Compare two variants and return winner per metric."""
    required = {"strength_mpa", "lcc", "predicted_service_life_years"}
    missing_left = required - left.keys()
    missing_right = required - right.keys()
    if missing_left or missing_right:
        raise ValueError("Both variants must include strength_mpa, lcc and predicted_service_life_years")

    result = {
        "strength_mpa": "left" if left["strength_mpa"] >= right["strength_mpa"] else "right",
        "lcc": "left" if left["lcc"] <= right["lcc"] else "right",
        "predicted_service_life_years": (
            "left" if left["predicted_service_life_years"] >= right["predicted_service_life_years"] else "right"
        ),
    }

    left_score = sum(1 for winner in result.values() if winner == "left")
    right_score = len(result) - left_score
    result["overall"] = "left" if left_score >= right_score else "right"
    return result
