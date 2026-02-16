from app.calculator import (
    add, subtract, multiply, divide, power, sqrt, factorial, average, maximum, minimum, mod, floor_divide
)

def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(10, 4) == 6

def test_multiply():
    assert multiply(3, 7) == 21

def test_divide():
    assert divide(10, 2) == 5

def test_power():
    assert power(2, 6) == 64

def test_sqrt():
    assert sqrt(81) == 9.0

def test_factorial():
    assert factorial(5) == 120

def test_average():
    assert average([10, 20, 30]) == 20.0

def test_max_min():
    assert maximum([1, 9, 3]) == 9
    assert minimum([1, 9, 3]) == 1

def test_mod_floor_divide():
    assert mod(10, 3) == 1
    assert floor_divide(10, 3) == 3
