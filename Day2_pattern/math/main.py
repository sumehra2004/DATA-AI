import math_util
a=int(input("Enter a value:"))
b=int(input("Enter b value:"))
print("MENU \n 1.add\n 2.subtraction \n 3.multiplication \n 4.division \n 5.remainder")
op=int(input("Enter operation to be performed:"))
if op==1:
    print(math_util.add(a,b))
elif op==2:
    print(math_util.sub(a,b))
elif op==3:
    print(math_util.mul(a,b))
elif op==4 :
    print(math_util.div(a,b))
elif op==5:
    print(math_util.remainder(a,b))
else:
    print("Invalid ")