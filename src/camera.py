import sys, time, random
from vec import *
from ray import *
from color import *
from scene import *
from hitinfo import *

class Camera:
    def __init__(self, samples, imgWidth, maxBounces) -> None:
        
        ## IMAGE VALUES
        self.imageAR = 16/9 # aspect ratio
        self.imageWidth = imgWidth
        self.imageHeight = max(1, int(self.imageWidth / self.imageAR))
        self.allPixels = self.imageHeight * self.imageWidth

        ## DETAIL SETTINGS
        self.samples = samples
        self.maxBounces = maxBounces

        self.focalLength = 1.0
        self.viewportH = 2.0
        self.viewportW = self.viewportH * self.imageWidth/self.imageHeight
        self.cameraCenter = point3(0,0,0)

        # size of the viewport
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
        ## THE ACTUAL FUNCTION THATS RENDERING THE SCENE AND PASSING THE RESULT TO THE RENDERTARGET
        
        # save starttime so we can calculate delta later on
        startTime = time.time()

        # loop throgh every pixel
        for y in range(self.imageHeight):
            for x in range(self.imageWidth):

                # print progress information
                pxLeft = self.allPixels - (y * self.imageWidth) + self.imageWidth - x
                sys.stdout.write("\r{0}".format("pixels remaining: "+ str(pxLeft) + "   "))
                sys.stdout.flush()

                # calculate the first ray thats shooting out of the camera
                pxCenter = self.originPixel + (x * self.pxDelta_u) + (y * self.pxDelta_v) 
                rayDirection = pxCenter - self.cameraCenter
                ray = Ray(self.cameraCenter, rayDirection) # not a unit vector
                
                color = col(0,0,0)
                for i in range(self.samples):
                    # shift the ray origin to sample different subpixels
                    sampleRay = ray
                    sampleRay.origin += (random.randint(-50, 50) / 100) * self.pxDelta_u +  (random.randint(-50, 50) / 100) * self.pxDelta_v

                    # add to pixel color by sending the first ray (will recursively bounce)
                    color += self.rayColor(sampleRay, scene, self.maxBounces)

                # average out the color from all samples and push it to the rendertartet
                renderTarget.push(x, y, ((color/self.samples).colToGammaSpace()))

        # retrurn rendering time
        return int(time.time()-startTime)


    def rayColor(self, ray:Ray, scene:Scene, bouncesleft:int) -> col:
        ## THIS FUNCTION DOES THE RAY-COLLISION CHECKS WITH ALL OBJECTS IN THE SCENE
        ## AND CALCULATES A FINAL COLOR. IT CALLS ITSELF RECURSIVELY TO BOUNCE THE RAY

        # tmin over 0 to avoid self-intersection due to floating point calculation errors
        tmin, tmax = 0.001, 99 

        # if the bouncelimit is reached we break out of the recursion loop 
        if bouncesleft <= 0:
            return col(0,0,0)

        # grab collision information with all objects in the scene (must not contain a collision)
        hitInfos = [object.checkCollision(ray, tmin, tmax) for object in scene.objects]
        
        # only keep collisions
        collisions = []
        for coll in hitInfos:
            if coll.didHit:
                collisions.append(coll)
        
        # did a collision happen?
        didCollide = len(collisions) > 0

        if not didCollide:
            # render sky
            unitDirection = normalize(ray.direction)
            lerpFac = 0.5 * (unitDirection.y+1)
            resColor = ((1-lerpFac) * col(1.0, 1.0, 1.0)) + (lerpFac * col(0.5, 0.7, 1.0)) # lerps between two colors 
            return resColor
        
        # if collision happened:

        #sort the list by distance of collision and get first object
        firstCollision = sorted(collisions, key=lambda x: x.t)[0] # sort by t and save first entry       
        t = firstCollision.t
        hitPoint = firstCollision.hitPoint
        normal = firstCollision.hitNormal
        material = firstCollision.hitMaterial
        incomingRay = firstCollision.ray

        color = col(0,0,0)
        # bounce the ray by recursion
        bounceRay, colo, ignore = material.scatter(incomingRay, normal, hitPoint)
        if not ignore:
            color = material.color * self.rayColor(bounceRay, scene, bouncesleft-1)

        #color = 0.5*col(normal.x+1, normal.y+1, normal.z+1) # uncomment for normal shading
        return color

        

        
        