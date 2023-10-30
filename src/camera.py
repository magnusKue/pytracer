import sys, time, random
from vec import *
from ray import *
from color import *
from scene import *
from hitinfo import *

class Camera:
    def __init__(self) -> None:
        self.imageAR = 16/9 # aspect ratio
        self.imageWidth = 800
        self.imageHeight = max(1, int(self.imageWidth / self.imageAR))
        self.allPixels = self.imageHeight * self.imageWidth

        self.samples = 50
        self.maxBounces = 10

        self.focalLength = 1.0
        self.viewportH = 2.0
        self.viewportW = self.viewportH * self.imageWidth/self.imageHeight
        self.cameraCenter = point3(0,0,0)

        self.viewPort_u = vec3(self.viewportW, 0, 0)
        self.viewPort_v = vec3(0, -self.viewportH, 0)

        # pixel to pixel spacing vectors
        self.pxDelta_u = self.viewPort_u / self.imageWidth
        self.pxDelta_v = self.viewPort_v / self.imageHeight

        # location of upper left corner
        self.viewportUpLeft = self.cameraCenter - vec3(0, 0, self.focalLength) - self.viewPort_u/2 - self.viewPort_v/2

        # location of first pixel
        self.originPixel = self.viewportUpLeft + 0.5 * (self.pxDelta_u + self.pxDelta_v)


    def render(self, renderTarget, scene, progressIndication=True):

        startTime = time.time()

        for y in range(self.imageHeight):
            for x in range(self.imageWidth):
                pxLeft = self.allPixels - (max(0, y-1) * self.imageWidth) + self.imageWidth - x
                sys.stdout.write("\r{0}".format("pixels remaining: "+ str(pxLeft) + "   "))
                sys.stdout.flush()

                pxCenter = self.originPixel + (x * self.pxDelta_u) + (y * self.pxDelta_v) 
                rayDirection = pxCenter - self.cameraCenter
                
                color = col(0,0,0)
                for i in range(self.samples):
                    ray = Ray(self.cameraCenter, rayDirection) # not a unit vector
                    ray.origin += (random.randint(-50, 50) / 100) * self.pxDelta_u +  (random.randint(-50, 50) / 100) * self.pxDelta_v
                    color += self.rayColor(ray, scene, self.maxBounces)

                renderTarget.push(x, y, ((color/self.samples).colToGammaSpace()))
        return int(time.time()-startTime)


    def rayColor(self, ray:Ray, scene:Scene, bouncesleft:int) -> col:
        tmin, tmax = 0.001, 99 # tmin over 0 to avoid self-intersection due to floating point calculation errors

        if bouncesleft <= 0:
            return col(0,0,0)

        # grab all collision information (must not contain a collision)
        hitInfos = [object.checkCollision(ray, tmin, tmax) for object in scene.objects]
        
        # only keep collition
        collisions = []
        for coll in hitInfos:
            if coll.didHit:
                collisions.append(coll)
        
        # did a collision happen?
        didCollide = len(collisions) > 0

        #sort the list by distance of collision and get first object
        if not didCollide:
            # render sky

            unitDirection = normalize(ray.direction)
            lerpFac = 0.5 * (unitDirection.y+1)
            resColor = ((1-lerpFac) * col(1.0, 1.0, 1.0)) + (lerpFac * col(0.5, 0.7, 1.0)) # lerps between two colors 
            return resColor

        # if collision happened:
        firstCollision = sorted(collisions, key=lambda x: x.t)[0] # sort by t and save first entry       
        t = firstCollision.t
        hitPoint = firstCollision.hitPoint
        normal = firstCollision.hitNormal
        material = firstCollision.hitMaterial
        incomingRay = firstCollision.ray

        # bounce
        color = col(0,0,0)
        bounceRay, colt, ignore = material.scatter(incomingRay, normal, hitPoint)
        if not ignore:
            color = material.color * self.rayColor(bounceRay, scene, bouncesleft-1)

        #color = 0.5*col(normal.x+1, normal.y+1, normal.z+1) # normal shading
        return color

        

        
        