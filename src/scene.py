from ray import *
from vec import *
from color import *
from math import sqrt, floor

class Scene:
    def __init__(self):
        self.objects = []

    def addObject(self, object):
        self.objects.append(object)

class Object:
    def __init__(self):
        pass

    def checkCollision(self, r, tmin, tmax):
        pass

class Sphere(Object):
    def __init__(self, pos:point3, radius, color:col):
        super().__init__()
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
    
class Floor(object):
    def __init__(self, yPos, color1, color2):
        super().__init__()
        self.yPos = yPos.y
        self.color1 = color1
        self.color2 = color2

    def checkCollision(self, r:Ray, tmin, tmax):
        if r.direction.y >= 0:
            # no intersection
            return False, None, None, None, None
        
        t = float(self.yPos / float(r.direction.y))

        point = r.origin + (t*r.direction)
        normal = vec3(0,1,0)
        
        scale = 5
        if point.x % scale > 0.5*scale:
            fac = .5
        else: fac = -.5

        if point.z % scale > 0.5*scale:
            fac *= -1

        fac += .5
        fac *= 255

        color = col(fac,fac,fac)

        return True, t, point, normal, color
        