# class Demo:
#     def add(self, a, b):
#         return a + b

#     def add(self, a, b, c):
#         return a + b + c    
    
# d = Demo()
# result1 = d.add(2, 3) 

# class Demo:
#     def add(self, *args):
#         if len(args) == 2:
#             return args[0] + args[1]
#         elif len(args) == 3:
#             return args[0] + args[1] + args[2]  

# d = Demo()
# result1 = d.add(2, 3)   
# print("Sum of 2 numbers:", result1)
# result2 = d.add(2, 3, 4)        
# print("Sum of 3 numbers:", result2)

class display:
    def show(self,*args):
        if len(args) == 1:
            print("one:",args[0])
        elif len(args) == 2:
            print("two:",args[0],args[1])
        else:
            print("none")

d=display()
d.show(10)  
d.show("sum",20)
d.show("s")
d.show()