import os, sys, time, datetime, random

from vec import *
from color import *
from ray import *
from hitinfo import *
from material import *
from camera import *
import rendertarget

samples = 10
imgWidth = 400
maxBounces = 10

camera = Camera(samples=samples, imgWidth=imgWidth, maxBounces=maxBounces)
scene = Scene()

# place spheres at random position with randomized size and material
random.seed(124413) 
for x in range(100):
    color = col(random.uniform(0,1),random.uniform(0,1),random.uniform(0,1))
    mat = random.choice([Metal(color, random.uniform(0,1)), Lambertian(color)])
    diameter = random.uniform(.1, 2)
    scene.addObject(Sphere(
                pos=point3(random.randint(-20, 20),diameter*.5,-random.randint(1, 50)),
                radius=diameter*2,
                material= mat
            )
        )
 
scene.addObject(Floor(
        point3(0,-1,0), 
        col(0.8,0.1,0.1), 
        col(.7,.8,.8),
        material = Lambertian(col(0.8, 0.8, 0.0))
    )
)

# set the rendertartet which the color data will be sent to after rendering
rt = rendertarget.PygameWIN(
    resolution=[camera.imageWidth, camera.imageHeight],
    maxColorValue=255,
    path="C:\\Users\\Magnus\\Magnus\\Code\\py\\raytracer\\v01\\pytracer\\output\\output2.ppm"
)

os.system('cls')

# render the scene
deltaT = camera.render(renderTarget=rt, scene=scene)        

os.system('cls')
print(f"rendered {camera.imageWidth} x {camera.imageHeight} pixels in {str(datetime.timedelta(seconds=deltaT))}s")

rt.finish()