# Create a class called Circle with two members x, y (center of the circle ) and r
# being the radius.
# The class must contain a methods called circumference and area compute
# them using the formulas circumference = 2*pi*r and area = pi * r2.
class Circle:
    x=''
    y=''
    r=''
    def __init__(self,x,y,r):
        self.x=x
        self.y=y
        self.r=r
        self.pi=3.142
        
    def circumference(self):
        return 2*self.pi*self.r
    
    def area(self):
        return self.pi*pow(self.r,2)
    
cir=Circle(3,4,5)
print("circumference=",cir.circumference(),"/n area=",cir.area())