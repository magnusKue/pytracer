import sys, time, random
from vec import *
from ray import *
from color import *
from scene import *
from collisions import *

class Camera:
    def __init__(self) -> None:
        self.imageAR = 16/9 # aspect ratio
        self.imageWidth = 400
        self.imageHeight = max(1, int(self.imageWidth / self.imageAR))

        self.samples = 1

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

            sys.stdout.write("\r{0}".format("scanlines remaining: "+ str(self.imageHeight-y-1) + " "))
            sys.stdout.flush()

            for x in range(self.imageWidth):
                pxCenter = self.originPixel + (x * self.pxDelta_u) + (y * self.pxDelta_v) 
                rayDirection = pxCenter - self.cameraCenter
                
                color = col(0,0,0)
                for x in range(self.samples):
                    ray = Ray(self.cameraCenter, rayDirection) # not a unit vector
                    ray.origin += (random.randint(-50, 50) / 100) * self.pxDelta_u +  (random.randint(-50, 50) / 100) * self.pxDelta_v
                    color += self.rayColor(ray, scene)

                renderTarget += str(color/self.samples)
        
        return int(time.time()-startTime), renderTarget

    def rayColor(self, ray:Ray, scene:Scene) -> col:
        tmin, tmax = 0, 99

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
        collisionPoint = firstCollision.hitPoint
        normal = firstCollision.hitNormal
        color = firstCollision.hitMaterial.color

        # bounce
        #bounceRay = 
        #bounceColor = self.rayColor(ray, scene:Scene)

        #color = 0.5*col(normal.x+1, normal.y+1, normal.z+1) # normal shading
        return color

        

        
        