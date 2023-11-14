import sys, random, argparse, pathlib

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # disable annoying pygame welcome message
 
from vec import *
from color import *

from camera import *
import rendertarget, material

defaultSamples = 50
defaultAR = 16/9
defaultImageWidth = 400
defaultBounceCap = 6

parser = argparse.ArgumentParser(description='\x1b[1;32;40mA simple python raytracer\x1b[0m')
color = '\x1b[0;33;40m'
colorEnd = '\x1b[0m'
parser.add_argument('--scene', "-S", "-scn", type=str, help=color+'Load a scene from world.json. No defaults'+colorEnd)
parser.add_argument('--samples', "-s", "-smp", type=int, help=color+f'Number of samples per pixel. Default is {defaultSamples}'+colorEnd)
parser.add_argument('--bounces', "-b", "-bnc", type=int, help=color+f'Ray bounce cap. Default is {defaultBounceCap}'+colorEnd)
parser.add_argument('--resolution', "-r", "-res", type=str, help=color+f'Image resolution as WIDTHxHEIGHT (Bsp: "600x400"). Default is {defaultImageWidth}x{max(1, int(defaultImageWidth / defaultAR))}'+colorEnd)
args = parser.parse_args()

res = None
if args.res:
    res = [int(args.res.split("x")[0]), int(args.res.split("x")[1])]


camera = Camera(
    samples=args.samples if args.samples else defaultSamples, 
    aspectRatio= max(1, float(res[0]/res[1])) if res else defaultAR,
    imgWidth=res[0] if res else defaultImageWidth, # note: if not given the height is calculated from the width and the aspect ratio
    maxBounces=args.bounces if args.bounces else defaultBounceCap, 
    ambientOcclusion=col(.4, .4, .8),
    useSky=True
)



scene = Scene(
    AO=col(1,1,1),
    useSky=True
)
scene.load(args.scene if args.scene else "scene1")

random.seed(24453)

# set the rendertartet which the color data will be sent to after rendering
rt = rendertarget.PygameWIN(
    resolution=[camera.imageWidth, camera.imageHeight],
    maxColorValue=255,
    path= pathlib.Path(__file__).resolve().parent / pathlib.Path("../output/output2.ppm")
)

# render the scene and get time diff
deltaTime = camera.render(renderTarget=rt, scene=scene)        

rt.finish(deltaT = deltaTime)