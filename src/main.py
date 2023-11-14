import sys, random, argparse, pathlib 
from colorama import init as colorama_init
from colorama import Fore, Back, Style
colorama_init()

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # disable annoying pygame welcome message
 
from vec import *
from color import *

from camera import *
import rendertarget, material

defaultSamples = 50
defaultAR = 16/9
defaultImageWidth = 5
defaultBounceCap = 6
defaultDest = pathlib.Path(__file__).resolve().parent / pathlib.Path("../output.ppm")

parser = argparse.ArgumentParser(description=f'{Back.GREEN}{Fore.BLACK} - A simple python raytracer - {Style.RESET_ALL}')

parser.add_argument('--scene', "-S", "-scn", type=str, help=f"{Fore.GREEN}Load a scene from world.json. {Fore.RED}No defaults{Style.RESET_ALL}")
parser.add_argument('--samples', "-s", "-smp", type=int, help=f'{Fore.GREEN}Number of samples per pixel. {Fore.RED}Default is {defaultSamples}{Style.RESET_ALL}')
parser.add_argument('--bounces', "-b", "-bnc", type=int, help=f'{Fore.GREEN}Ray bounce cap. {Fore.RED}Default is {defaultBounceCap}{Style.RESET_ALL}')
parser.add_argument('--resolution', "-r", "-res", type=str, help=f'{Fore.GREEN}Image resolution as WIDTHxHEIGHT (Bsp: "600x400"). {Fore.RED}Default is {defaultImageWidth}x{max(1, int(defaultImageWidth / defaultAR))}{Style.RESET_ALL}')
parser.add_argument('--destination', "-d", "-dest", type=str, help=f'{Fore.GREEN}Path to the rendered image. {Fore.RED}Default is {pathlib.Path(__file__).resolve().parent / pathlib.Path("../output.ppm")}{Style.RESET_ALL}')
args = parser.parse_args()

res = None
if args.resolution:
    res = [int(args.resolution.split("x")[0]), int(args.resolution.split("x")[1])]


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
    path= args.destination if args.destination else defaultDest
)

# render the scene and get time diff
deltaTime = camera.render(renderTarget=rt, scene=scene)        

rt.finish(deltaT = deltaTime)