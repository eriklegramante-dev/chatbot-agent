"""
Mathematical tools for CrewAI agent execution.
"""

from crewai.tools import tool


@tool("Add numbers")
def add(a: float, b: float) -> float:
    """
    Adds two numbers together and returns the sum.

    :param a: The first number.
    :param b: The second number.
    :return: Sum of a and b.
    """
    return float(a) + float(b)


@tool("Subtract numbers")
def subtract(a: float, b: float) -> float:
    """
    Subtracts the second number from the first number.

    :param a: The base number.
    :param b: The number to subtract.
    :return: Difference of a and b.
    """
    return float(a) - float(b)


@tool("Multiply numbers")
def multiply(a: float, b: float) -> float:
    """
    Multiplies two numbers together.

    :param a: First factor.
    :param b: Second factor.
    :return: Product of a and b.
    """
    return float(a) * float(b)


@tool("Divide numbers")
def divide(a: float, b: float) -> float:
    """
    Divides the first number by the second number.

    :param a: Dividend.
    :param b: Divisor.
    :return: Quotient of division.
    """
    if float(b) == 0:
        raise ValueError("Cannot divide by zero.")
    return float(a) / float(b)
