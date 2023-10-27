import os, sys, time

from vec import *
from color import *
from ray import *
from collisions import *
from camera import *

camera = Camera()
scene = Scene()
scene.addObject(Sphere(
            pos=point3(-2,0,-4),
            radius=.6,
            color = col(0,0,255)
        )
    )

scene.addObject(Sphere(
            pos=point3(2,0,-4),
            radius=1,
            color = col(255,0,0)
        )
    )
scene.addObject(Floor(point3(0,-1,0), col(0,0,0), col(255,255,255)))

maxColorVal = 255
rendertarget = ""
rendertarget += f"P3\n{camera.imageWidth} {camera.imageHeight} \n{maxColorVal}\n" # file header

os.system('cls')
deltaT, rendertarget = camera.render(renderTarget=rendertarget, scene=scene)        

with open("C:\\Users\\Magnus\\Magnus\\Code\\py\\raytracer\\v01\\pytracer\\output\\output2.ppm", "w") as fp:
    fp.write(rendertarget)

os.system('cls')
print(f"done in {deltaT}s")
