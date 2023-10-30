from ray import *
from color import *

class Material:
    def __init__(self, color:col):
        self.color = color

    def scatter(self, ray:Ray, normal, hitPoint):
        pass

class Lambertian(Material):
    def __init__(self, color: col):
        super().__init__(color)

    def scatter(self, ray: Ray, normal, hitPoint):
        scatteredRay = Ray(hitPoint, vec3.randomInUnitSphere() + normal)
        if scatteredRay.direction.isNearZero():
            scatteredRay.direction = normal
        return scatteredRay, self.color, False
    
class Metal(Material):
    def __init__(self, color: col, fuzz):
        super().__init__(color)
        self.fuzz = fuzz

    def scatter(self, ray: Ray, normal, hitPoint):
        vecIn = ray.direction
        reflected = reflect(normalize(vecIn), normal)
        scatteredRay = Ray(hitPoint, reflected + self.fuzz * vec3.randomInUnitSphere())
        ignore = not dot(scatteredRay.direction, normal) > 0
        return scatteredRay, self.color, ignore