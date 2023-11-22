# Create a class called Stack and implement the methods to push, pop and
# head using a list for storing the elements.

class Stack:
    def __init__(self):
        self.list=[]
    
    def push(self,ele):
        self.list.append(ele)
        print(ele," pushed into stack")
    
    def pop(self):
        if(len(self.list)==0):
            print("stack is empty")
            return
        ele=self.list.pop()
        print(ele," popped from stack")
    
    def head(self):
        return self.list[-1]
        
stack=Stack()
print(stack.push(3))
print(stack.push(4))
print(stack.push(5))
print(stack.push(6))
print(stack.pop())
