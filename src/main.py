import os, sys, time, datetime, random

from vec import *
from color import *
from ray import *
from hitinfo import *
from material import *
from camera import *
import rendertarget

samples = 50
imgWidth = 500
maxBounces = 20

camera = Camera(samples=samples, imgWidth=imgWidth, maxBounces=maxBounces)
scene = Scene()

# place spheres at random position with randomized size and material

for x in range(5):
    scene.addObject(Sphere(
                pos=point3(-4 + x*2, 1, -4),
                radius=1,
                material= Metal(col(1, 1, 1), 1-(.25*x))
            )
        )
 
scene.addObject(Floor(
        yPos = point3(0, -1, 0), 
        color1 = col(0.8 ,0.1, 0.1), 
        color2 = col(0.7, 0.8, 0.8),
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