import os, sys, time, datetime, random

from vec import *
from color import *
from ray import *
from hitinfo import *
from camera import *
import rendertarget, material

camera = Camera(
    samples=3, 
    aspectRatio=16/9,
    imgWidth=100, 
    maxBounces=6, 
    ambientOcclusion=col(1, 1, 1)
)
scene = Scene()

# place spheres at random position with randomized size and material
random.seed(24453)

scene.addObject(
        Sphere(
            pos=point3(0, 0, -6),
            radius=4,
            material=material.Metal(col(0.4,0.4,0.1), 1)
        )
    )

# scene.addObject(Floor(
#         yPos = point3(0, -1, 0), 
#         color1 = col(0.9 ,0.9, 0.9), 
#         color2 = col(0.1, 0.1, 0.1),
#         material = material.Emmisive(col(0.008, 0.008, 0.0))
#     )
# )


# set the rendertartet which the color data will be sent to after rendering
rt = rendertarget.PygameWIN(
    resolution=[camera.imageWidth, camera.imageHeight],
    maxColorValue=255,
    path="C:\\Users\\Magnus\\Magnus\\Code\\py\\raytracer\\v01\\pytracer\\output\\output2.ppm"
)

# render the scene
deltaT = camera.render(renderTarget=rt, scene=scene)        

rt.finish(deltaT = deltaT)