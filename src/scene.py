from ray import *
from vec import *
from color import *
from hitinfo import *
from material import *
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
    def __init__(self, pos:point3, radius, material:Material):
        super().__init__()
        self.position = pos
        self.radius = radius
        self.material = material
    
    def checkCollision(self, r, tmin, tmax):
        super().checkCollision(r, tmin, tmax)
        
        oc = r.origin - self.position
        a = r.direction.lengthSquared()
        halfb = dot(oc, r.direction)
        c = oc.lengthSquared() - self.radius * self.radius
        discriminant  = halfb * halfb - a * c
        if discriminant < 0:
            # no collision
            return HitInfo.zero()
        
        sqrtD = sqrt(discriminant)
        root = (-halfb - sqrtD) / a

        if root <= tmin or tmax <= root:
            root = (-halfb + sqrtD) / a
            if root <= tmin or tmax <= root:
                # no collision
                return HitInfo.zero()
            
        t = root
        collisionPoint = r.step(t)

        normal = (collisionPoint - self.position) / self.radius # normalized outward-pointing normal

        return HitInfo(True, t, collisionPoint, normal, self.material, r)
    
class Floor(object):
    def __init__(self, yPos, color1, color2, material):
        super().__init__()
        self.yPos = yPos.y
        self.color1 = color1
        self.color2 = color2
        self.material = material # this should never be seen

    def checkCollision(self, r:Ray, tmin, tmax):
        if r.direction.y >= 0:
            return HitInfo.zero()
        
        t = float(self.yPos / float(r.direction.y))

        point = r.origin + (t*r.direction)
        normal = vec3(0,1,0)
        
        scale = 5
        if point.x % scale > 0.5*scale:
            fac = .5
        else: fac = -.5

        if point.z % scale > 0.5*scale:
            fac *= -1

        if fac == -0.5:
            self.material.color = self.color1
        else:
            self.material.color = self.color2
            
        return HitInfo(True, t, point, normal, self.material, r)
        