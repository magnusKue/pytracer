import sys, random, argparse, pathlib 


import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # disable annoying pygame welcome message
 
from vec import *
from color import *

from argParser import Parser
from camera import *
import rendertarget, material
from error import Error

argParser = Parser(
    defaultSamples = 30,
    defaultImageWidth = 200,
    defaultImageHeight = 160,
    defaultBounceCap = 4,
    defaultDest = pathlib.Path(__file__).resolve().parent / pathlib.Path("../output.ppm"),
    defaultPreview = True,
    defaultWhite = False
)
args = argParser.getArgs()

camera = Camera(
    samples=args.samples, 
    imgWidth=int(argParser.resolution[0]) if args.resolution else argParser.defaultImageWidth, # note: if not given the height is calculated from the width and the aspect ratio
    imgHeight=int(argParser.resolution[1]) if args.resolution else argParser.defaultImageHeight,
    maxBounces=args.bounces, 
    ambientLight=col(.4, .4, .8),
    useSky=True
)

scene = Scene(
    ambientLight=col(1,1,1),
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
try:
    deltaTime = camera.render(renderTarget=rt, scene=scene)        
except KeyboardInterrupt:
    Error.raiseError(
        type="Rendering interrupted",
        info="quitting.",
        quitSrc=True
    )

# keep preview window alive
rt.finish(deltaT = deltaTime)