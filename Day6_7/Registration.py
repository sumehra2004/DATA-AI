# def registration(func):
#     def wrapper(email,username, password):
#         if len(password) < 8:
#             print("Password must be at least 8 characters long.")
#         elif "@" not in email or "." not in email:
#             print("Invalid email format.")
#         else:
#             func(email,username, password)
#     return wrapper
# @registration
# def register_user(email,username, password):
#     print(f"Registration Successfully Completed .Welcome to dashboard!")
# email = input("Enter your email: ")
# username = input("Enter your username: ")
# password = input("Enter your password: ")
# register_user(email,username, password)

def registration(func):
    def wrapper(*args,**kwargs):
        is_registered=True
        if is_registered:
            return func(*args,**kwargs)
        else:   
            print("Register first.")
    return wrapper
@registration
def view_course_details(course_name):
    print(f"Accessing course:{course_name}")
view_course_details("Python Basics")
     