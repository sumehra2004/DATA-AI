class Employee:
    def __init__(self, emp_id, name, salary, designation):
        self.emp_id = emp_id
        self.name = name
        self.salary = salary
        self.designation = designation

    def display(self):
        print("Employee ID:", self.emp_id)
        print("Name:", self.name)
        print("Salary:", self.salary)
        print("Designation:", self.designation)
