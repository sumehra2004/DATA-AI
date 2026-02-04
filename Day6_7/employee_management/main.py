from decorators import registration, login
from employee import Employee

is_logged_in = False

@registration
def after_registration(username):
    print(f"Welcome {username}")
    print("You can now login.")

@login
def show_dashboard():
    print("\nEmployee Dashboard")
    emp.display()

emp = Employee(101, "Alice", 50000, "Developer")


while True:
    print("\n===== EMPLOYEE MANAGEMENT SYSTEM =====")
    print("1. Register")
    print("2. Login")
    print("3. View Employee Details")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        email = input("Enter email: ")
        username = input("Enter username: ")
        password = input("Enter password: ")
        after_registration(email, username, password)

    elif choice == "2":
        is_logged_in = True
        print("Login flag set to TRUE")

    elif choice == "3":
        show_dashboard(is_logged_in)

    elif choice == "4":
        print("Exiting... Thank you!")
        break

    else:
        print("Invalid choice")
