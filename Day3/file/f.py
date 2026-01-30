# file=open("notes.txt","w")
# file.write("This is my first note.\n")
# file.write("This is my second note.\n")
# file.close()

# file=open("notes.txt","r")
# content=file.read()
# print(content)
# file.close()

# file=open("notes.txt","a")
# file.write("This is my third note.\n")
# file.close()

# with open("notes.txt","r") as file:
#     content=file.read()
#     print(content)

# feedback=input("Enter your feedback: ")
# with open("feedback.txt","a") as file:
#     file.write(feedback+"\n")   
# print("Thank you for your feedback!")

# with open("data.txt", "r") as file:
#     print(file.readline().strip())
#     print(file.readline().strip())
#     print(file.readline().strip())

# with open("data.txt", "r") as file:
#     while True:
#         line = file.readline()
#         if not line:
#             break
#         print(line.strip())