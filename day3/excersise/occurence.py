sentence="she sells a sea shell in the sea shore"
dict={}
list=sentence.split(" ")
for word in list:
    if(word in dict):
        dict[word]+=1
    else:
        dict[word]=1

# dict[word]=dict.get(word,0)+1    //altenative method 
print(dict)
