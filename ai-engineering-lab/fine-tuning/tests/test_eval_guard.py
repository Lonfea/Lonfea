import pytest

from app.evaluate import compare


def test_forgetting_guard_passes_small_drop():
    summary = compare(
        {"domain_accuracy": 0.70, "general_accuracy": 0.90},
        {"domain_accuracy": 0.82, "general_accuracy": 0.89},
    )
    assert summary.general_drop == pytest.approx(0.01)


def test_forgetting_guard_blocks_large_drop():
    with pytest.raises(RuntimeError, match="catastrophic forgetting"):
        compare(
            {"domain_accuracy": 0.70, "general_accuracy": 0.90},
            {"domain_accuracy": 0.82, "general_accuracy": 0.80},
        )
