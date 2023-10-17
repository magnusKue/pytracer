from vec import *
from ray import *

def hitSphere(center:point3, radius:float, ray:Ray) -> bool:
    oc = ray.origin - center
    
    a = dot(ray.direction, ray.direction)
    b = 2.0 * dot(oc, ray.direction)
    c = dot(oc, oc) - radius * radius

    discriminant = b * b - 4 * a * c
    return discriminant >= 0