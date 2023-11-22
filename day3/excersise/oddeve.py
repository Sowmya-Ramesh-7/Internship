a=[*range(0,100)]
eve=[]
odd=[]
for i in a:
    if i%2==0:
        eve.append(i)
    else:
        odd.append(i)
print(eve)
