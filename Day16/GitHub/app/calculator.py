"""Super Calculator

This module is used by tests and the CI/CD pipeline.
"""

from __future__ import annotations

import math
from typing import Iterable, Union

Number = Union[int, float]

# ---------- Basic ----------
def add(a: Number, b: Number) -> Number:
    return a + b

def subtract(a: Number, b: Number) -> Number:
    return a - b

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

# ---------- Advanced ----------
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

# ---------- Tiny CLI (optional) ----------
def main() -> None:
    print("=== Super Calculator ===")
    print("1) add  2) subtract  3) multiply  4) divide")
    print("5) power  6) sqrt  7) factorial  8) average")
    print("9) max  10) min  0) exit")

    while True:
        try:
            choice = int(input("Enter choice: ").strip())
        except ValueError:
            print("Enter a number.")
            continue

        if choice == 0:
            print("Bye!")
            break

        try:
            if choice in (1,2,3,4,5):
                a = float(input("a: "))
                b = float(input("b: "))
                if choice == 1: print("Result:", add(a,b))
                elif choice == 2: print("Result:", subtract(a,b))
                elif choice == 3: print("Result:", multiply(a,b))
                elif choice == 4: print("Result:", divide(a,b))
                elif choice == 5: print("Result:", power(a,b))

            elif choice == 6:
                x = float(input("x: "))
                print("Result:", sqrt(x))

            elif choice == 7:
                n = int(input("n (int): "))
                print("Result:", factorial(n))

            elif choice == 8:
                raw = input("Enter numbers comma-separated: ")
                nums = [float(x.strip()) for x in raw.split(",") if x.strip()]
                print("Result:", average(nums))

            elif choice == 9:
                raw = input("Enter numbers comma-separated: ")
                nums = [float(x.strip()) for x in raw.split(",") if x.strip()]
                print("Result:", maximum(nums))

            elif choice == 10:
                raw = input("Enter numbers comma-separated: ")
                nums = [float(x.strip()) for x in raw.split(",") if x.strip()]
                print("Result:", minimum(nums))
            else:
                print("Invalid choice.")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
