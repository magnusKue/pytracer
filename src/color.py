import math
from ray import *

class col:
    def __init__(self, r, g, b) -> None:
        self.r = r
        self.g = g
        self.b = b
    
    def __add__(self, o):
        return col(
            self.r + o.r,
            self.g + o.g,
            self.b + o.b
        )
    
    def __iadd__(self, o):
        return self + o

    def __sub__(self, o):
        return col(
            self.r + o.r,
            self.g + o.g,
            self.b + o.b
        )
    
    def __isub__(self, o):
        return self - o
    
    def __mul__(self, o):
        if isinstance(o, self.__class__):
            return col(
                self.r * o.r,
                self.g * o.g,
                self.b * o.b
            )
        elif isinstance(o, int) or isinstance(o, float):
            return col(
                self.r * o,
                self.g * o,
                self.b * o
            )
        else:
            raise TypeError("vector multiplication only supports other vectors, integers or floats") 
    
    __rmul__ = __mul__

    def __imul__(self, o):
        return self * o

    def __truediv__(self, o:int | float):
        return (1/o) * self
    
    def __itruediv__(self, o):
        return self / o
    
    def __str__(self) -> str:
        return f"{255.999*self.r} {255.999*self.g} {255.999*self.b}\n"
    
    def componentToGamma(self, comp):
        return math.sqrt(comp)

    def colToGammaSpace(self):
        return col(
            self.componentToGamma(self.r),
            self.componentToGamma(self.g),
            self.componentToGamma(self.b)
        )


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