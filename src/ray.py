from vec import *

class Ray:
    def __init__(self, origin:point3, direction:vec3) -> None:
        self.origin = origin
        self.direction = direction

    def getOrigin(self):
        return self.origin
    
    def getDirection(self):
        return self.direction
    
    def step(self, t):
        return self.origin + (t * self.direction)
    


