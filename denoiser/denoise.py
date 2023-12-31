import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from tkinter import *
from tkinter import filedialog, messagebox

srcFullpath = filedialog.askopenfilename(initialdir = "/",title = "Select sorce",filetypes = (("PNG","*.png*"),("PPM","*.ppm*"),("all files","*.*")))
srcName = srcFullpath.split("/")[-1]
srcPath = srcFullpath[:-len(srcName)]

destPath = filedialog.askdirectory(initialdir = "/",title = "Select destination")
destFullPath = destPath+"/"+srcName[:-4]+"_denoised.png"
print(destFullPath)
intensity = 6  # default ~7

img = cv.imread(srcFullpath)
img = cv.fastNlMeansDenoisingColored(img,None,intensity,intensity,7,21)
cv.imwrite(destFullPath, img)

messagebox.showinfo("showinfo", "Saved denoised image successfully") 

# switch color chanels to correctly display in matplot
# red = img[:,:,2].copy()
# blue = img[:,:,0].copy()

# img[:,:,0] = red
# img[:,:,2] = blue

# plt.imshow(img)
# plt.show()