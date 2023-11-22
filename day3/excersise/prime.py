list=[1,2,3]
flag=True
for num in list:
    if num>2:
        for i in range(2,num):
            if num%i==0:
                flag=False
                break
        if flag==False:
            break
        
print(flag)
        
            
    