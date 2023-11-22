# Create a class called Point with two members x, y both being integers.
# The class must contain a method called distance which can calculate the
# distance between two points. Formula for the distance between two points =
# (x2 - y2).
import math
class Point:
    x=''
    y=''
    def __init__(self,x,y):
        self.x=x
        self.y=y
        
    def distance(self,point):
        return math.sqrt((self.x-point.x)**2+(self.y-point.y)**2)
    
point1=Point(3,4)
point2=Point(4,5)
print(point1.distance(point2))