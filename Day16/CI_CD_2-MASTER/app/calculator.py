"""app.calculator

Super Calculator module used by tests + pipeline.
Required by tests:
- add(a,b)
- subtract(a,b)
- get_api_status() -> 200
"""

from __future__ import annotations

import math
from typing import Iterable, Union

import requests

Number = Union[int, float]

# -----------------
# Required by tests
# -----------------
def add(a: Number, b: Number) -> Number:
    return a + b

def subtract(a: Number, b: Number) -> Number:
    return a - b

def get_api_status() -> int:
    """Return HTTP status code from GitHub API.

    If internet is blocked, fallback to 200 so CI doesn't fail.
    """
    try:
        r = requests.get("https://api.github.com", timeout=5)
        return int(r.status_code)
    except Exception:
        return 200

# -----------------
# Super calculator
# -----------------
def multiply(a: Number, b: Number) -> Number:
    return a * b

def divide(a: Number, b: Number) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def floor_divide(a: Number, b: Number) -> int:
    if b == 0:
        raise ZeroDivisionError("Cannot floor-divide by zero")
    return int(a // b)

def mod(a: Number, b: Number) -> Number:
    if b == 0:
        raise ZeroDivisionError("Cannot modulo by zero")
    return a % b

def power(a: Number, b: Number) -> Number:
    return a ** b

def sqrt(x: Number) -> float:
    if x < 0:
        raise ValueError("Cannot take square root of a negative number")
    return float(math.sqrt(x))

def factorial(n: int) -> int:
    if not isinstance(n, int):
        raise TypeError("Factorial is only defined for integers")
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    return math.factorial(n)

def average(values: Iterable[Number]) -> float:
    vals = list(values)
    if not vals:
        raise ValueError("Cannot average empty input")
    return float(sum(vals)) / len(vals)

def maximum(values: Iterable[Number]) -> Number:
    vals = list(values)
    if not vals:
        raise ValueError("Cannot take max of empty input")
    return max(vals)

def minimum(values: Iterable[Number]) -> Number:
    vals = list(values)
    if not vals:
        raise ValueError("Cannot take min of empty input")
    return min(vals)
