# employee.py

class Employee:

    def __init__(self, emp_id, name, salary):
        self.emp_id = emp_id
        self.name = name
        self.salary = salary

    def increase_salary(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")

        self.salary += amount
        return self.salary

    def decrease_salary(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")

        if amount > self.salary:
            raise ValueError("Cannot decrease more than salary")

        self.salary -= amount
        return self.salary

    def get_annual_salary(self):
        return self.salary * 12

    def is_high_earner(self):
        return self.salary >= 50000
