str="HelLo WorLd"
count=0
for i in range(0,4):
    if(str[i].isupper):
        count+=1
        
if(count>2):
    print(str.upper())
else:
    print(str)