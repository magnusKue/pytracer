from vec import *
from ray import *
from math import sqrt

def hitSphere(center, radius, r):
    oc = r.origin - center
    a = dot(r.direction, r.direction)
    b = 2.0 * dot(oc, r.direction)
    c = dot(oc, oc) - radius*radius
    discriminant = b*b - 4*a*c

    if discriminant < 0:
        return -1.0
    else:
        return (-b - sqrt(discriminant) ) / (2.0*a)
    
class hitRecord:
    def __init__(self) -> None:
        self.p = point3(0,0,0)
        self.normal = vec3(0,0,0)
        self.t = 0

        self.frontFace = None

    def setFaceNormal(self, r:Ray, outwardNormal:vec3): # outwardNormal expects unit vector
        # set normal vector 
        self.frontFace = dot(r.direction, outwardNormal) < 0 # if positive: ray is inside sphere |else: ray is outside
        
        if self.frontFace:
            self.normal = outwardNormal
        else: self.normal = -outwardNormal

class hittable:
    def __init__(self) -> None:
        pass

    def hit(r:Ray, ray_tmin, ray_tmax, rec:hitRecord):
        pass

class Sphere(hittable):
    def __init__(self, center, radius) -> None:
        super().__init__()
        self.center = center
        self.radius = radius

    def hit(self, r:Ray, ray_tmin, ray_tmax, rec:hitRecord):
        super().hit(r, ray_tmin, ray_tmax, rec)

        oc = r.origin - self.center
    
        a = r.direction.lengthSquared()
        halfb = dot(oc, r.direction)
        c = oc.lengthSquared() - self.radius * self.radius

        discriminant  = halfb * halfb - a * c

        if discriminant < 0:
            return False
        
        sqrtD = sqrt(discriminant)
        root = (-halfb - sqrtD) / a

        if root <= ray_tmin or ray_tmax <= root:
            root = (-halfb + sqrtD) / a
            if root <= ray_tmin or ray_tmax <= root:
                return False
            
        rec.t = root
        rec.p = r.step(rec.t)

        outwardNormal = (rec.p - self.center) / self.radius 
        rec.setFaceNormal(r, outwardNormal)

        return True 