from src.tools.tools import add, subtract, multiply, divide


def test_arithmetic_tools():
    assert add.func(10, 5) == "15"
    assert subtract.func(10, 5) == "5"
    assert multiply.func(4, 3) == "12"
    assert divide.func(10, 2) == "5"
    assert "Division by zero" in divide.func(5, 0)
