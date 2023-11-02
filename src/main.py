import os, sys, time, datetime, random

from vec import *
from color import *
from ray import *
from hitinfo import *
from material import *
from camera import *
import rendertarget

camera = Camera(
    samples=180, 
    aspectRatio=16/9,
    imgWidth=800, 
    maxBounces=3, 
    ambientOcclusion=col(0.01, 0.01, 0.04)
)
scene = Scene()

# place spheres at random position with randomized size and material
random.seed(24453)


scene.addObject(
        Sphere(
            pos=point3(-6, 2, -8),
            radius=4,
            material=Emmisive(col(100,100,100))
        )
    )

scene.addObject(
        Sphere(
            pos=point3(2.1, 1, -8),
            radius=2,
            material=Lambertian(col(1,0,0))
        )
    )

scene.addObject(Floor(
        yPos = point3(0, -1, 0), 
        color1 = col(0.9 ,0.9, 0.9), 
        color2 = col(0.1, 0.1, 0.1),
        material = Lambertian(col(0.8, 0.8, 0.0))
    )
)


# set the rendertartet which the color data will be sent to after rendering
rt = rendertarget.PygameWIN(
    resolution=[camera.imageWidth, camera.imageHeight],
    maxColorValue=255,
    path="C:\\Users\\Magnus\\Magnus\\Code\\py\\raytracer\\v01\\pytracer\\output\\output2.ppm"
)

# render the scene
deltaT = camera.render(renderTarget=rt, scene=scene)        

rt.finish(deltaT = deltaT)