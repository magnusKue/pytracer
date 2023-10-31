import os, sys, time, datetime, random

from vec import *
from color import *
from ray import *
from hitinfo import *
from material import *
from camera import *
import rendertarget

samples = 150
imgWidth = 900
maxBounces = 60

camera = Camera(samples=samples, imgWidth=imgWidth, maxBounces=maxBounces)
scene = Scene()

# place spheres at random position with randomized size and material
random.seed(24453)

scene.addObject(
    Sphere(
        pos=point3(8, 2, -2),
        radius=4,
        material=Metal(col(.647,.5,.38), 0)
    )
)

scene.addObject(
    Sphere(
        pos=point3(-8, 2, -2),
        radius=4,
        material=Metal(col(.24,.44,.41), 0)
    )
)

scene.addObject(
    Sphere(
        pos=point3(7.5, 4, -16),
        radius=4,
        material=Lambertian(col(.53,.023,.09))
    )
)

scene.addObject(
    Sphere(
        pos=point3(-7.5, 4, -16),
        radius=4,
        material=Lambertian(col(.161,.2,.361))
    )
)

scene.addObject(
    Sphere(
        pos=point3(0, 2, -12),
        radius=4,
        material=Metal(col(.95,.99,.82), 1)
    )
)

scene.addObject(Floor(
        yPos = point3(0, -1, 0), 
        color1 = col(0.5 ,0.78, 0.4), 
        color2 = col(0.4, 0.5, 0.8),
        material = Metal(col(0.8, 0.8, 0.0), .3)
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