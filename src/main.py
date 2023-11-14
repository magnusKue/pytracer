import sys, random, argparse, pathlib

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # disable annoying pygame welcome message
 
from vec import *
from color import *

from camera import *
import rendertarget, material


parser = argparse.ArgumentParser(description='A simple python raytracer')

parser.add_argument('--scene', "-S", type=str, help='Load a scene from world.json')
parser.add_argument('--samples', "-s", type=int, help='Number of samples per pixel')
parser.add_argument('--bounces', "-b", type=int, help='Ray bounce cap. Default is 6')
parser.add_argument('--res', "-r", type=str, help='Image resolution as WIDTHxHEIGHT (Bsp: "600x400")')
args = parser.parse_args()

res = None
if args.res:
    res = [int(args.res.split("x")[0]), int(args.res.split("x")[1])]

camera = Camera(
    samples=args.samples if args.samples else 3, 
    aspectRatio= max(1, float(res[0]/res[1])) if res else 16/9,
    imgWidth=res[0] if res else 400, # note: if not given the height is calculated from the width and the aspect ratio
    maxBounces=args.bounces if args.bounces else 3, 
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