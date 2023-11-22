print("enter words separaed by comma:")
words=input()
list=words.split(",")
print(list)
longest=list[0]
length=len(list[0].strip())

for word in list:
    currlen=len(word.strip())
    if(length<currlen):
        length=currlen
        longest=word

print("longest word is",longest," it is of length ",length)
