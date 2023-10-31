import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from tkinter import *
from tkinter import filedialog

srcFullpath = filedialog.askopenfilename(initialdir = "/",title = "Select sorce",filetypes = (("PNG","*.png*"),("PPM","*.ppm*"),("all files","*.*")))
srcName = srcFullpath.split("/")[-1]
srcPath = srcFullpath[:-len(srcName)]

srcFullpath = filedialog.askdirectory(initialdir = "/",title = "Select destination")


img = cv.imread(srcFullpath)


intensity = 5

img = cv.fastNlMeansDenoisingColored(img,None,intensity,intensity,7,21)
cv.imwrite(srcFullpath+srcName[:-4]+"_denoised.png", img)

# switch color chanels to correctly display in matplot
red = img[:,:,2].copy()
blue = img[:,:,0].copy()

img[:,:,0] = red
img[:,:,2] = blue

plt.imshow(img)
plt.show()