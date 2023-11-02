import os, sys, time, datetime, random

from vec import *
from color import *
from ray import *
from hitinfo import *
from material import *
from camera import *
import rendertarget

camera = Camera(
    samples=100, 
    aspectRatio=16/9,
    imgWidth=100, 
    maxBounces=60, 
    ambientOcclusion=col(0.01, 0.01, 0.04)
)
scene = Scene()

# place spheres at random position with randomized size and material
random.seed(24453)


scene.addObject(
        Sphere(
            pos=point3(0, 1, -4),
            radius=2,
            material=Emmisive(col(1,1,1))
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