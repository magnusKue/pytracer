import os, sys, time, datetime

from vec import *
from color import *
from ray import *
from collisions import *
from camera import *

camera = Camera()
scene = Scene()
scene.addObject(Sphere(
            pos=point3(-1.5,0,-4),
            radius=2,
            material= Lambertian(col(1,0,0))
        )
    )

scene.addObject(Sphere(
            pos=point3(1.5,0,-4),
            radius=1,
            material= Lambertian(col(0,0,1))
        )
    )
scene.addObject(Floor(
        point3(0,-1,0), 
        col(1,0,0), 
        col(1,1,1),
        material = Metal(col(1,.07,.46))
    )
)

maxColorVal = 255
rendertarget = ""
rendertarget += f"P3\n{camera.imageWidth} {camera.imageHeight} \n{maxColorVal}\n" # file header

os.system('cls')
deltaT, rendertarget = camera.render(renderTarget=rendertarget, scene=scene)        

with open("C:\\Users\\Magnus\\Magnus\\Code\\py\\raytracer\\v01\\pytracer\\output\\output2.ppm", "w") as fp:
    fp.write(rendertarget)

os.system('cls')
print(f"rendered {camera.imageWidth} x {camera.imageHeight} pixels in {str(datetime.timedelta(seconds=deltaT))}s")
