import re

username = input("Enter username: ")
password = input("Enter password: ")

if re.match(r"^[a-zA-Z0-9]{5,}", username):
    print("Username is valid")
else:
    print("Invalid username")

if re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).{8,}", password):
    print("Password is strong")
else:
    print("Password is weak")