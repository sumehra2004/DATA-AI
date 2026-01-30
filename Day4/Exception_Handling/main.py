# print("Step1")
# a=10
# b=20
# res=a/b
# print("step2")
# print("Result is:",res)

# try:
#     print("Step1")
#     a = int(input("Enter numerator: "))
#     b = int(input("Enter denominator: "))
#     res = a / b
#     print("step2")
#     print("Result is:", res)
# except ZeroDivisionError:
#     print("Error: Division by zero is not allowed.")

try:
    print("Step1")
    a = int(input("Enter numerator: "))
    b = int(input("Enter denominator: "))
    res = a / b
    print("step2")
    print("Result is:", res)
except Exception as e:
    print("Error occurred:", e)
finally:
    print("Execution completed.")
