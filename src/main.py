import os, sys, time

from vec import *
from color import *
from ray import *
from collisions import *

def rayColor(r:Ray) -> col:
    t = hitSphere(point3(0, 0, -1), 0.5, r)
    if t > 0.0:
        surfaceNormal = unitize(r.step(t) - vec3(0,0,-1))
        return 0.5*col(surfaceNormal.x+1, surfaceNormal.y+1, surfaceNormal.z+1)

    unitDirection = unitize(r.direction)
    lerpFac = 0.5 * (unitDirection.y+1)
    resColor = ((1-lerpFac) * col(1.0, 1.0, 1.0)) + (lerpFac * col(0.5, 0.7, 1.0)) # lerps between two colors 
    return resColor

# Image

imageAR = 16/9 # aspect ratio
imageWidth = 400
imageHeight = int(imageWidth / imageAR)
if imageHeight < 1: imageHeight = 1

# Camera

focalLength = 1.0
viewportH = 2.0
viewportW = viewportH * imageWidth/imageHeight
cameraCenter = point3(0,0,0)

# Viewport edges 
viewPort_u = vec3(viewportW, 0, 0)
viewPort_v = vec3(0, -viewportH, 0)

# pixel to pixel spacing vectors
pxDelta_u = viewPort_u / imageWidth
pxDelta_v = viewPort_v / imageHeight

# location of upper left corner
viewportUpLeft = cameraCenter - vec3(0,0,focalLength) - viewPort_u/2 - viewPort_v/2

# location of first pixel
originPixel = viewportUpLeft + 0.5 * (pxDelta_u + pxDelta_v)

# Render

maxColorVal = 255

output = ""
output += f"P3\n{imageWidth} {imageHeight} \n{maxColorVal}\n" # file header

os.system('cls')
startTime = time.time()

for y in range(imageHeight):
    sys.stdout.write("\r{0}".format("scanlines remaining: "+ str(imageHeight-y-1) + " "))
    sys.stdout.flush()

    for x in range(imageWidth):
        pxCenter = originPixel + (x * pxDelta_u) + (y * pxDelta_v) 
        rayDirection = pxCenter - cameraCenter

        ray = Ray(cameraCenter, rayDirection) # note: not a unit vector
        
        #color = col(x/(imageWidth-1), y/(imageHeight-1), 0) # uv map coloring
        output += str(rayColor(ray))
        

with open("C:\\Users\\Magnus\\Magnus\\Code\\py\\raytracer\\v01\\pytracer\\output\\output2.ppm", "w") as fp:
    fp.write(output)

#os.system('cls')
print(f"done in {int(time.time()-startTime)}s")
