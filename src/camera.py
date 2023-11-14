import sys, time, random, datetime
from vec import *
from ray import *
from color import *
from scene import *
from hitinfo import *

class Camera:
    def __init__(self, samples:int, aspectRatio:float, imgWidth:int, maxBounces:int, ambientOcclusion:col=col(0,0,0), useSky=False) -> None:
        
        ## IMAGE VALUES
        self.imageAR = aspectRatio # aspect ratio
        self.imageWidth = imgWidth
        self.imageHeight = max(1, int(self.imageWidth / self.imageAR))
        self.allPixels = self.imageHeight * self.imageWidth

        ## SETTINGS
        self.samples = samples
        self.maxBounces = maxBounces
        self.ambientOcclusion = ambientOcclusion
        self.useSky = False

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

        self.startTime = time.time()
        # loop throgh every pixel
        for y in range(self.imageHeight):
            for x in range(self.imageWidth):
                # calculate the first ray thats shooting out of the camera
                pxCenter = self.originPixel + (x * self.pxDelta_u) + (y * self.pxDelta_v) 
                rayDirection = pxCenter - self.cameraCenter
                
                color = col(0,0,0)
                for i in range(self.samples):
                    sampleRay = Ray(self.cameraCenter, rayDirection) # not a unit vector
                    # shift the ray origin to sample different subpixels
                    sampleRay.origin += random.uniform(-.5, .5) * self.pxDelta_u +  random.uniform(-.5, .5) * self.pxDelta_v

                    # add to pixel color by sending the first ray (will recursively bounce)
                    color += self.rayColor(sampleRay, scene, self.maxBounces)

                # average out the color from all samples and push it to the rendertartet
                renderTarget.push(x, y, (color/self.samples).colToGammaSpace())

    def rayColor(self, ray:Ray, scene:Scene, bouncesleft:int) -> col:
        ## THIS FUNCTION DOES THE RAY-COLLISION CHECKS WITH ALL OBJECTS IN THE SCENE
        ## AND CALCULATES A FINAL COLOR. IT CALLS ITSELF RECURSIVELY TO BOUNCE THE RAY.
        ## THE RECURSION IS BROKEN THROUGH THE BOUNCE CAP OR WHEN NO COLLISION OCCURED

        # if the bouncelimit is reached we break out of the recursion loop 
        if bouncesleft <= 0:
            return col(0,0,0)

        # grab collision information with all objects in the scene (must not contain a collision)
        tmin, tmax = 0.001, 99  # tmin over 0 to avoid self-intersection due to floating point calculation errors
        hitInfos = [object.checkCollision(ray, tmin, tmax) for object in scene.objects] 
        collisions = [col for col in hitInfos if col.didHit] # remove all empty collision objects
        
        # return sky if and break out of recursion loop if no collision happened
        if not collisions:
            return scene.sky.getSkyColor(ray)
        

        #sort the list by distance of collision and get first object
        firstCollision = sorted(collisions, key=lambda x: x.t)[0] # sort by t and save first entry       
        
        # store frist hit material as a variable because it is used often
        material = firstCollision.hitMaterial

        scatterInfoObj = material.scatter(firstCollision.ray, firstCollision.hitNormal, firstCollision.hitPoint)
        
        if scatterInfoObj.ignore:
            return material.emitted()

        # bounce the ray by recursion and accumulate the light into one color
        colorFromScatter = scatterInfoObj.color * self.rayColor(scatterInfoObj.rayOut, scene, bouncesleft-1)
        # get emitted color if object emmits light
        colorFromEmission = material.emitted()

        #color = 0.5*col(normal.x+1, normal.y+1, normal.z+1) # uncomment for normal shading
        return colorFromScatter + colorFromEmission

        

        

        
        