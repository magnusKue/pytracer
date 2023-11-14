from ray import *
from vec import *
from color import *
from hitinfo import *
from material import *
from math import sqrt, floor
import json, pathlib

## THIS FILE DEFINES OBJECTS BY GIVING THEM A RAY COLLISION FUNCTION THAT RETURNS A HITINFO

class Scene:
    ## THIS CLASS HOLDS OUR WORLD AND ALL OBJECT INSTANCES
    def __init__(self, AO, useSky):
        self.sky = Sky(AO=AO, useSky=useSky)
        self.objects = []
        self.path = pathlib.Path(__file__).resolve().parent / pathlib.Path("..\\world.json")

    def addObject(self, object):
        self.objects.append(object)

    def load(self, scene):
        with open(self.path, 'r') as world:
            data = json.load(world)[scene]
        self.sky.ambientOcclusion = listToCol(data["ambient_occlusion"])
        self.sky.useSky = data["use_sky_gradient"]

        for obj in data["objects"]:
            mat = None

            color = col(.9,.9,.9)
            if obj["type"] != "floor":
                color = listToCol(obj["material"]["color"])
            
            match obj["material"]["type"]:
                case "emissive":
                    mat = Emissive(color)
                case "lambertian":
                    mat = Lambertian(color)
                case "metal":
                    mat = Metal(color, fuzz=int(obj["material"]["fuzz"])) 
                case _:
                    mat = Lambertian(color)

            match obj["type"]:
                case "sphere":
                    self.addObject(Sphere(
                        pos = listToPoint(obj["position"]),
                        radius = int(obj["radius"]),
                        material = mat
                    ))
                case "floor":
                    self.addObject(Floor(
                        pos = listToPoint(obj["position"]),
                        color1 = listToCol(obj["color1"]),
                        color2 = listToCol(obj["color2"]),
                        material = mat
                    ))

class Object:
    def __init__(self):
        pass

    def checkCollision(self, r, tmin, tmax):
        pass

class Sky:
    def __init__(self, useSky, AO):
        self.useSky = useSky
        self.ambientOcclusion = AO

    def getSkyColor(self, ray):
        if not self.useSky:
            return self.ambientOcclusion
        else:
            # render sky by belending between two colors depending on the ray "angle" and scaling the result by the ambient occlusion
            unitDirection = normalize(ray.direction)
            lerpFac = 0.5 * (unitDirection.y+1)
            resColor = ((1-lerpFac) * col(1.0, 1.0, 1.0)) + (lerpFac * col(0.5, 0.7, 1.0)) # lerps between two colors 
            return resColor * self.ambientOcclusion 

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
    def __init__(self, pos:vec3, color1:col, color2:col, material:Material):
        super().__init__()
        self.yPos = pos.y
        self.color1 = color1
        self.color2 = color2
        self.material = material # default color should never be seen

    def checkCollision(self, r:Ray, tmin:int, tmax:int):
        if r.direction.y >= 0:
            return HitInfo.zero()
        
        t = float(self.yPos / float(r.direction.y))

        if t > tmax or t < tmin:
            return HitInfo.zero()

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
        