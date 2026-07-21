import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tools import add, divide, multiply, subtract


def test_add_valid_numbers():
    assert add(5, 4) == 9.0
    assert add(-1, 1) == 0.0


def test_subtract_valid_numbers():
    assert subtract(10, 2) == 8.0


def test_multiply_valid_numbers():
    assert multiply(3, 4) == 12.0


def test_divide_valid_and_by_zero():
    assert divide(10, 2) == 5.0
    assert "Error: Division by zero" in divide(5, 0)


def test_guardrail_invalid_text_inputs():
    expected_error = "Error: Invalid arguments"

    assert expected_error in add("5", "potato")
    assert expected_error in divide("word", 2)