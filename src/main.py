import os, sys, time, datetime

from vec import *
from color import *
from ray import *
from hitinfo import *
from material import *
from camera import *
import rendertarget

camera = Camera()
scene = Scene()
scene.addObject(Sphere(
            pos=point3(-2,0,-4),
            radius=1,
            material= Metal(col(0.8, 0.8, 0.8), 0)
        )
    )

scene.addObject(Sphere(
            pos=point3(0,0,-4),
            radius=1,
            material= Lambertian(col(0.7, 0.3, 0.3))
        )
    )

scene.addObject(Sphere(
            pos=point3(2,0,-4),
            radius=1,
            material= Metal(col(0.8, 0.6, 0.2), 1)
        )
    )

scene.addObject(Floor(
        point3(0,-1,0), 
        col(0.8,0.1,0.1), 
        col(.7,.8,.8),
        material = Lambertian(col(0.8, 0.8, 0.0))
    )
)

rt = rendertarget.PygameWIN(
    resolution=[camera.imageWidth, camera.imageHeight],
    maxColorValue=255,
    path="C:\\Users\\Magnus\\Magnus\\Code\\py\\raytracer\\v01\\pytracer\\output\\output2.ppm"
)

os.system('cls')
deltaT = camera.render(renderTarget=rt, scene=scene)        

os.system('cls')
print(f"rendered {camera.imageWidth} x {camera.imageHeight} pixels in {str(datetime.timedelta(seconds=deltaT))}s")

rt.finish()