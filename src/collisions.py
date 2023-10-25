from vec import *
from ray import *
from math import sqrt

def hitSphere(center:point3, radius:float, ray:Ray) -> bool:
    oc = ray.origin - center
    
    a = dot(ray.direction, ray.direction)
    b = 2.0 * dot(oc, ray.direction)
    c = dot(oc, oc) - radius * radius

    discriminant  = b * b - 4 * a * c
    if discriminant < 0:
        return -1
    else:
        return (-b - sqrt(discriminant) ) / (2.0*a)