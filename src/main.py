import sys, random, argparse, pathlib 


import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # disable annoying pygame welcome message
 
from vec import *
from color import *

from argParser import Parser
from camera import *
import rendertarget, material

argParser = Parser(
    defaultSamples = 150,
    defaultAR = 16/9,
    defaultImageWidth = 400,
    defaultBounceCap = 4,
    defaultDest = pathlib.Path(__file__).resolve().parent / pathlib.Path("../output.ppm"),
    defaultPreview = True,
    defaultWhite = False
)
args = argParser.getArgs()

res = None
if args.resolution:
    res = [int(args.resolution.split("x")[0]), int(args.resolution.split("x")[1])]


camera = Camera(
    samples=args.samples, 
    aspectRatio= max(1, float(res[0]/res[1])) if res else argParser.defaultAR,
    imgWidth=res[0] if res else argParser.defaultImageWidth, # note: if not given the height is calculated from the width and the aspect ratio
    maxBounces=args.bounces, 
    ambientOcclusion=col(.4, .4, .8),
    useSky=True
)

scene = Scene(
    AO=col(1,1,1),
    useSky=True
)
scene.load(args.scene)

random.seed(24453)

# set the rendertartet which the color data will be sent to after rendering
if args.preview:
    rt = rendertarget.PygameWIN(
        resolution=[camera.imageWidth, camera.imageHeight],
        maxColorValue=255,
        path= args.destination,
        useWhite= args.usewhite
    )
else:
    rt = rendertarget.PPM(
        resolution=[camera.imageWidth, camera.imageHeight],
        maxColorValue=255,
        path = args.destination,
        useWhite= args.usewhite
    )

# render the scene and get time diff

deltaTime = camera.render(renderTarget=rt, scene=scene)        

rt.finish(deltaT = deltaTime)