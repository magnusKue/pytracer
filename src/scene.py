from ray import *
from vec import *
from color import *
from math import sqrt

class Scene:
    def __init__(self):
        self.objects = []

    def addObject(self, object):
        self.objects.append(object)

class Object:
    def __init__(self, pos, color):
        self.position = pos
        self.color = color

    def checkCollision(self, r, tmin, tmax):
        pass

class Sphere(Object):
    def __init__(self, pos:point3, radius, color:col):
        super().__init__(pos, color)
        self.position = pos
        self.radius = radius
        self.color = color
    
    def checkCollision(self, r, tmin, tmax):
        super().checkCollision(r, tmin, tmax)
        
        oc = r.origin - self.position
        a = r.direction.lengthSquared()
        halfb = dot(oc, r.direction)
        c = oc.lengthSquared() - self.radius * self.radius
        discriminant  = halfb * halfb - a * c
        if discriminant < 0:
            # no collision
            return False, None, None, None, None
        
        sqrtD = sqrt(discriminant)
        root = (-halfb - sqrtD) / a

        if root <= tmin or tmax <= root:
            root = (-halfb + sqrtD) / a
            if root <= tmin or tmax <= root:
                # no collision
                return False, None, None, None, None
            
        t = root
        collisionPoint = r.step(t)

        normal = (collisionPoint - self.position) / self.radius # normalized outward-pointing normal

        return True, t, collisionPoint, normal, self.color