list=[1,2,3,4,1,3,43,1,4,2,2]
dict={}
for i in list:
    dict[i]=dict.get(i,0)+1 
print(dict)