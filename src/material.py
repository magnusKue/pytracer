from ray import *
from color import *

## MATERIALS ARE DEFINED BY THEIR COLOR AND THE WAY THEY REDIRECT RAYS, HITTING THEIR SURFACE. 
## THIS PROPERTY IS DESCRIBED IN THE SCATTER FUNTCTION.

class ScatterInfo:
    def __init__(self, rayOut, color, ignore) -> None:
        self.rayOut = rayOut
        self.color = color
        self.ignore = ignore

    @staticmethod
    def ignoreScatter():
        return ScatterInfo(rayOut=None, color=None, ignore=True)

class Material:
    def __init__(self, color:col):
        self.color = color

    def scatter(self, ray:Ray, normal, hitPoint):
        pass 

    def emitted(self):
        return col(0,0,0)

class Lambertian(Material):
    ## BASIC DIFFUSE MATERIAL, RANDOMLY SCATTERING RAYS
    def __init__(self, color: col):
        super().__init__(color)

    def scatter(self, ray: Ray, normal, hitPoint):
        scatteredRay = Ray(hitPoint, vec3.randomInUnitSphere() + normal)
        if scatteredRay.direction.isNearZero():
            scatteredRay.direction = normal
        return ScatterInfo(rayOut=scatteredRay, color=self.color, ignore=False)
    
class Metal(Material):
    ## REFLECTIVE SURFACE, PERFECTLY MIRRORING AN INCOMING RAY
    def __init__(self, color: col, fuzz):
        super().__init__(color)
        self.fuzz = fuzz

    def scatter(self, ray: Ray, normal, hitPoint):
        vecIn = ray.direction

        # reflects the incoming vector by the normal
        reflected = reflect(normalize(vecIn), normal)
        
        # we shift the ray direction to blur the reflection
        scatteredRay = Ray(hitPoint, reflected + self.fuzz * vec3.randomInUnitSphere())

        # if we accidentaly shifted the ray to point inside of the object, we flag it so its ignored later on
        ignore = not dot(scatteredRay.direction, normal) > 0

        return ScatterInfo(rayOut=scatteredRay, color=self.color, ignore=ignore)

class Emissive(Material):
    def __init__(self, color: col):
        super().__init__(color)

    def scatter(self, ray: Ray, normal, hitPoint):
        # set ignore flag to true so the ray is not scattered
        return ScatterInfo.ignoreScatter()
    
    def emitted(self):
        return self.color