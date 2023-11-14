import os, sys, time, datetime, random

from vec import *
from color import *
from ray import *
from hitinfo import *
from camera import *
import rendertarget, material

camera = Camera(
    samples=50, 
    aspectRatio=16/9,
    imgWidth=400, # note: the height is calculated from the width and the aspect ratio
    maxBounces=6, 
    ambientOcclusion=col(.4, .4, .8),
    useSky=True
)
scene = Scene()

random.seed(24453)
# place spheres

############# SETUP SCENE ################
for x in range(5):
    scene.addObject(    
            Sphere(
                pos=point3(-4+2*x, .5, -6),
                radius=1,
                material=material.Metal(col(.8,.8,.3), x * .25)
            )
        )

scene.addObject(Floor(
        yPos = point3(0, -1, 0), 
        color1 = col(0.9 ,0.01, 0.01), 
        color2 = col(.9, .9, .9),
        material = material.Lambertian(col(0.008, 0.008, 0.0))
    )
)
##########################################

# set the rendertartet which the color data will be sent to after rendering
rt = rendertarget.PygameWIN(
    resolution=[camera.imageWidth, camera.imageHeight],
    maxColorValue=255,
    path="C:\\Users\\Magnus\\Magnus\\Code\\py\\raytracer\\v01\\pytracer\\output\\output2.ppm"
)

if sys.version_info[0:2] != (3, 10):
    raise Exception('Requires python 3.10')

# render the scene and get time diff
deltaTime = camera.render(renderTarget=rt, scene=scene)        

rt.finish(deltaT = deltaTime)