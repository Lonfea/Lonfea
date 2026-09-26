from app.risk import assess_uncertainty


def test_missing_context_is_high_risk():
    result = assess_uncertainty("This might be correct.", 0)
    assert result.score >= 0.6
    assert "no_validated_context" in result.reasons


def test_confident_grounded_answer_is_lower_risk():
    result = assess_uncertainty("The validated context states the target is 42.", 3)
    assert result.score < 0.5
