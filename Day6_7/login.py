def login_validator(func):
    def wrapper(login):
        if login:
            print("Login successful")
            func()
        else:
            print("Login failed")
    return wrapper
@login_validator
def access_dashboard():
    print("Accessing dashboard...")
login=input("Enter login status (True/False): ")
access_dashboard(login.capitalize())

