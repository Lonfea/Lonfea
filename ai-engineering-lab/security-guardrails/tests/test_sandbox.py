import pytest

from app.sandbox import UnsafeExpression, safe_calculate


def test_arithmetic_is_allowed():
    assert safe_calculate("(2 + 3) * 4") == 20.0


def test_function_calls_are_blocked():
    with pytest.raises(UnsafeExpression):
        safe_calculate("__import__('os').system('id')")


def test_attributes_are_blocked():
    with pytest.raises(UnsafeExpression):
        safe_calculate("(1).__class__")
