import pytest
from src.tools.tools import add, subtract, multiply, divide


def test_arithmetic_tools():
    assert add.func(10, 5) == 15.0
    assert subtract.func(10, 5) == 5.0
    assert multiply.func(4, 3) == 12.0
    assert divide.func(10, 2) == 5.0


def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        divide.func(5, 0)
