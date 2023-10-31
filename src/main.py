import os, sys, time, datetime, random

from vec import *
from color import *
from ray import *
from hitinfo import *
from material import *
from camera import *
import rendertarget

samples = 125
imgWidth = 300
maxBounces = 60

camera = Camera(samples=samples, imgWidth=imgWidth, maxBounces=maxBounces)
scene = Scene()

# place spheres at random position with randomized size and material
random.seed(24453)

scene.addObject(
    Sphere(
        pos=point3(8, 2, -10),
        radius=4,
        material=Metal(col(.8,.8,.8), 0)
    )
)
scene.addObject(
    Sphere(
        pos=point3(5, 2, -16),
        radius=4,
        material=Metal(col(.8,.8,.8), .5)
    )
)
scene.addObject(
    Sphere(
        pos=point3(1, 2, -24),
        radius=4,
        material=Metal(col(.8,.8,.8), 1)
    )
)

for x in range(100):
    radius = random.uniform(.1, .5)
    scene.addObject(Sphere(
                pos=point3(random.randint(-15, 15), -1+radius, -random.randint(-2, 40)),
                radius=radius,
                material= Lambertian(col(random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)))
            )
        )

scene.addObject(Floor(
        yPos = point3(0, -1, 0), 
        color1 = col(0.1 ,0.1, 0.1), 
        color2 = col(0.7, 0.8, 0.8),
        material = Metal(col(0.8, 0.8, 0.0), 1)
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