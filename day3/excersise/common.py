#atleast 1 common member among 2 lists
list=[1,2,3,4]
list2=[2,3,6]
flag=False
for i in list:
    if i in list2:
        flag=True
        break

print(flag)