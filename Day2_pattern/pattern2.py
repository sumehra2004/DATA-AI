'''for i in range(0,3):
    for j in range(0,3):
        if i==1 and j==1:
            print(" ",end=" ")
        else:
            print("* ",end="")
    print()'''

n = 3
for i in range(n):
    for j in range(n):
        if i == 0 or i == n-1 or j == 0 or j == n-1:
            print("*", end=" ")
        else:
            print(" ", end=" ")
    print()