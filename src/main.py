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
    imgWidth=100, # note: the height is calculated from the width and the aspect ratio
    maxBounces=6, 
    ambientOcclusion=col(.4, .4, .8),
    useSky=True
)
scene = Scene(
    AO=col(1,1,1),
    useSky=True
)
scene.load("scene1")

random.seed(24453)

# set the rendertartet which the color data will be sent to after rendering
rt = rendertarget.PygameWIN(
    resolution=[camera.imageWidth, camera.imageHeight],
    maxColorValue=255,
    path="pytracer\output\output2.ppm"
)

# render the scene and get time diff
deltaTime = camera.render(renderTarget=rt, scene=scene)        

rt.finish(deltaT = deltaTime)