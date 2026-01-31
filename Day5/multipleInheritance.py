# #Multiple Inheritance
# class Father:
#     def drive(self):
#         print("Father can drive")
# class Mother:
#     def cook(self):
#         print("Mother can cook")
# class Child(Father, Mother):
#     def play(self):
#         print("Child can play")

# c1=Child()
# c1.drive()
# c1.cook()
# c1.play()


# class A:
#     def display(self):
#         print("Display from class A")


# class B:
#     def display(self):
#         print("Display from class B")


# class C(B,A):   # C inherits from A and B
#     pass


# obj = C()
# obj.display()

class A:
    def display(self):
        print("Info from A")
        super().display()   # go to next class in MRO


class B:
    def display(self):
        print("Info from B")


class C(A, B):
    pass

obj = C()
obj.display()