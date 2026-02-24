import pytest
from employee import Employee


# ---------------- FIXTURE ----------------
@pytest.fixture
def employee():
    # default employee for testing
    return Employee(1, "John", 40000)


# ---------------- BUSINESS LOGIC TESTING ----------------
def test_annual_salary(employee):
    assert employee.get_annual_salary() == 40000 * 12


def test_high_earner_true():
    emp = Employee(2, "Alice", 60000)
    assert emp.is_high_earner() is True


def test_high_earner_false(employee):
    assert employee.is_high_earner() is False


# ---------------- PARAMETRIZED TESTING ----------------
@pytest.mark.parametrize("amount, expected", [
    (5000, 45000),
    (10000, 50000),
])
def test_increase_salary(employee, amount, expected):
    employee.salary = 40000  # reset salary
    assert employee.increase_salary(amount) == expected


@pytest.mark.parametrize("amount, expected", [
    (5000, 35000),
    (10000, 30000),
])
def test_decrease_salary(employee, amount, expected):
    employee.salary = 40000  # reset salary
    assert employee.decrease_salary(amount) == expected


# ---------------- EXCEPTION TESTING ----------------
@pytest.mark.parametrize("amount", [0, -100])
def test_increase_salary_invalid(employee, amount):
    with pytest.raises(ValueError, match="Amount must be positive"):
        employee.increase_salary(amount)


@pytest.mark.parametrize("amount", [0, -200])
def test_decrease_salary_invalid(employee, amount):
    with pytest.raises(ValueError, match="Amount must be positive"):
        employee.decrease_salary(amount)


def test_decrease_more_than_salary(employee):
    with pytest.raises(ValueError, match="Cannot decrease more than salary"):
        employee.decrease_salary(50000)
