import os, sys, time

from vec import *
from color import *

# Image

imageWidth = 256
imageHeight = 256

maxColorVal = 255

# Render

output = ""
output += f"P3\n{imageWidth} {imageHeight} \n{maxColorVal}\n"

os.system('cls')

for y in range(imageHeight):
    sys.stdout.write("\r{0}".format("scanlines remaining: "+ str(imageHeight-y-1)))
    sys.stdout.flush()

    for x in range(imageWidth):
        color = col(x/(imageWidth-1), y/(imageHeight-1), 0)
        output += str(color)

with open("C:\\Users\\Magnus\\Magnus\\Code\\py\\raytracer\\v01\\pytracer\\output\\output2.ppm", "w") as fp:
    fp.write(output)

os.system('cls')
print("done!")
