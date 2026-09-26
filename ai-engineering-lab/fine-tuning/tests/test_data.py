import pytest

from app.data import validate_preference_rows, validate_sft_rows


def test_sft_validation():
    validate_sft_rows([{"prompt": "Q", "completion": "A"}])


def test_preference_rejects_identical_answers():
    with pytest.raises(ValueError):
        validate_preference_rows(
            [{"prompt": "Q", "chosen": "same", "rejected": "same"}]
        )
