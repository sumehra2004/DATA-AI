import sys
'''var=sys.argv[1]
bar=sys.argv[2]
print(var,bar)'''
print("Enter prog:",sys.argv[0])
if len(sys.argv)>3:
    for i in range(1,len(sys.argv)):
        print(f"arg {i}:",sys.argv[i])
else :
    print(f"More than 2")
