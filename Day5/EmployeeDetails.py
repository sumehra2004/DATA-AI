class Employee:
    def __init__(self, name, emp_id, department):
        self.name = name
        self.emp_id = emp_id
        self.department = department

    def display_details(self):
        print("Employee Name:", self.name)
        print("Employee ID:", self.emp_id)
        print("Department:", self.department)
        print("----------------------")
employees = [] 

for i in range(3):
    print(f"\nEnter details for Employee {i+1}")
    name = input("Enter employee name: ")
    emp_id = input("Enter employee ID: ")
    department = input("Enter department: ")

    emp = Employee(name, emp_id, department)
    employees.append(emp)

print("\nEmployee Details\n")

for emp in employees:
    emp.display_details()
