import os

choice = input("Enter 1 to Add Task or 2 to View Tasks: ")

if choice == "1":
    with open("tasks.txt", "a") as f:
        f.write(input("Enter your task: ") + "\n")
    print("Task added!")

elif choice == "2":
    if os.path.exists("tasks.txt"):
        print("Your Tasks:")
        print(open("tasks.txt").read())
    else:
        print("No tasks found!")

else:
    print("Invalid choice!")


