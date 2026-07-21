"""
Mathematical Tools Module with Guardrails.
Contains basic operations protected against invalid arguments (text).
"""

from typing import Union


def add(a: float, b: float) -> Union[float, str]:
    """
    Adds two real numbers (a and b) and returns the result.
    Rule: Both arguments must be strict numbers.
    Use this tool when the user requests addition or sum.
    """
    try:
        return float(float(a) + float(b))
    except (ValueError, TypeError):
        return "Error: Invalid arguments. This tool accepts only real numbers, not text."


def subtract(a: float, b: float) -> Union[float, str]:
    """
    Subtracts the second number (b) from the first number (a) and returns the result.
    Rule: Both arguments must be strict numbers.
    Use this tool when the user requests subtraction or difference.
    """
    try:
        return float(float(a) - float(b))
    except (ValueError, TypeError):
        return "Error: Invalid arguments. This tool accepts only real numbers, not text."


def multiply(a: float, b: float) -> Union[float, str]:
    """
    Multiplies two real numbers (a and b) and returns the result.
    Rule: Both arguments must be strict numbers.
    Use this tool when the user requests multiplication or product.
    """
    try:
        return float(float(a) * float(b))
    except (ValueError, TypeError):
        return "Error: Invalid arguments. This tool accepts only real numbers, not text."


def divide(a: float, b: float) -> Union[float, str]:
    """
    Divides the first number (a) by the second number (b) and returns the result.
    Rules: Both arguments must be strict numbers and 'b' cannot be zero.
    Use this tool when the user requests division or quotient.
    """
    try:
        num_a = float(a)
        num_b = float(b)
        if num_b == 0:
            return "Error: Division by zero is not allowed."
        return float(num_a / num_b)
    except (ValueError, TypeError):
        return "Error: Invalid arguments. This tool accepts only real numbers, not text."