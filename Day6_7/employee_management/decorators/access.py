
def registration(func):
    def wrapper(email, username, password, *args):
        if len(password) < 8:
            print("Password must be at least 8 characters")
        elif "@" not in email or "." not in email:
            print("Invalid email format")
        else:
            print("Registration successful")
            return func(username, *args)
    return wrapper


def login(func):
    def wrapper(is_logged_in, *args):
        if is_logged_in:
            print("Login successful")
            return func(*args)
        else:
            print("Login failed. Access denied")
    return wrapper
