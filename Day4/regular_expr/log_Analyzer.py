import re

with open("app.log", "r") as file:
    logs = file.readlines()

error_count = 0

print("\n--- ERROR LOGS ---")
for line in logs:
    if re.search(r"ERROR.*", line):
        print(line.strip())
        error_count += 1

print("\nTotal Errors:", error_count)
