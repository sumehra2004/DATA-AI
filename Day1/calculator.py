def add(a,b):
    return a+b
def sub(a,b):
    return a-b
def mul(a,b):
    return a*b
def div(a,b):
    return a//b
def remainder(a,b):
    return a%b

a=int(input("Enter a value:"))
b=int(input("Enter b value:"))
print("MENU \n 1.add\n 2.subtraction \n 3.multiplication \n 4.division \n 5.remainder")
op=int(input("Enter operation to be performed:"))
if op==1:
    print(add(a,b))
elif op==2:
    print(sub(a,b))

elif op==3:
    print(mul(a,b))
elif op==4 :
    print(div(a,b))
elif op==5:
    print(remainder(a,b))
else:
    print("Invalid ")
