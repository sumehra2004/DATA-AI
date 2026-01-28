email=input("Enter email id :")
pwd=input("Enter password:")

if "@" not in email:
    print("Invalid email")
if len(pwd)<6:
    print("Invalid password")
else:
    print("Valid email with valid password \n form submitted successfully")

