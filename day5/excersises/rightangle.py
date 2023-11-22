# Create a class called Triangle with the angles of the three sides saved as
# members. Create a method called is_right_angled to verify if it is right
# angled.
class Triangle:
    x=''
    y=''
    z=''
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
        
    def is_right_angle(self):
        x2=self.x**2
        y2=self.y**2
        z2=self.z**2
        if(x2+y2==z2 or x2+z2==y2 or z2+y2==x2):
            return True
        else:
            return False
        
        
    
t=Triangle(3,4,5)
print(t.is_right_angle())