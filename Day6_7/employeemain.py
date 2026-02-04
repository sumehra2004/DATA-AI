from Employee import employee
e1 = employee.Employee(1, "Adi", 50000, "Developer")
e2 = employee.Employee(2, "Bina", 60000, "Tester")
e3 = employee.Employee(3, "John", 75000, "HR")
employees = [e1, e2, e3]
search_name = input("Enter employee name: ")
found = False
for emp in employees:
    if emp.name.lower() == search_name.lower():
        print("\n Employee Found")
        emp.display()
        found = True
        break
if not found:
    print("\n Employee not found")
