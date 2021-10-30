import cv2
import numpy as np
from math import sqrt

def circleDetect(img):
    # img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    c = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT,1,10,minRadius=10,maxRadius=50)
    c = c[0][0]
    #nerd shit but the /sqrt2 is a pretty nice thing about the ratio of an inscribed and circumscribed square around a circle
    #this here gives us the bit of the image that is entirely within the circle (means no background noise to poissibly effect image recognition)
        #yes this is overkill but if it didn't work because I didn't do this I would never code again
    img = img[
        int(c[1]-c[2]/sqrt(2)):int(c[1]+c[2]/sqrt(2)),
        int(c[0]-c[2]/sqrt(2)):int(c[0]+c[2]/sqrt(2))
    ]
    return img
fName = input('champ name') + '.jpg'

f = cv2.imread(fName, 0)
f = circleDetect(f)

cv2.imwrite(fName,f)
