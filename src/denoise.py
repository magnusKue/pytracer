import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

path = 'C:\\Users\\Magnus\\Magnus\\Code\\py\\raytracer\\v01\\pytracer\\results\\'
name = "final1.png"
img = cv.imread(path+name)


intensity = 5

img = cv.fastNlMeansDenoisingColored(img,None,intensity,intensity,7,21)
cv.imwrite(path+"denoised.png", img)

# switch color chanels to correctly display in matplot
red = img[:,:,2].copy()
blue = img[:,:,0].copy()

img[:,:,0] = red
img[:,:,2] = blue

plt.imshow(img)
plt.show()