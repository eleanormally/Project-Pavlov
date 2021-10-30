import os
from getWindow import getImage
try:
    from PIL import Image
except:
    import Image
import pytesseract as ocr
import cv2
import pandas #not really necessary but
from levenshtein import similarity
import numpy as np
from math import sqrt

from skimage.metrics import structural_similarity
import imutils

import taserTime

####Username stuff

#get tesseract
ocr.pytesseract.tesseract_cmd = r'C:\Users\me\AppData\Local\Tesseract-OCR\tesseract'

def getPosition(usernames):
    #get if a user has a similar enough username (in case OCR is doodoo)
    for i, u in enumerate(usernames):
        if similarity(u,'Heph3astus') < 3:
            return i

def doOCR(img):
    data = ocr.image_to_data(img, output_type='data.frame')
    #removes low confidence text that thank god is consistantly unimportant
    data = data[data.conf > 80]
        #the code gods smile upon me this midnight

    usernames = data['text'].tolist()
    return usernames

def positionList():
    #checks where player is in lineup so that their champion can be detected and they can be shocked
        #Note to self: why the fuck are you like this?
    img = getImage()
    return(getPosition(doOCR(img)))




####Image recognition stuff (cuz League's UI is dumb as hell for what I'm doing)

#gets box around champion circle so image recognition works more good
def circleDetect(img):
    img = cv2.cvtColor(np.array(img),cv2.COLOR_RGB2GRAY)
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


def victimsImage(victimPos):
    img = getImage(img=True)
    #splits into 5 different images
        #rounds off the bottom so pixels divisible by 5
    rFactor = len(img)%5
    img = img[:-rFactor,:]
    img = np.vsplit(img,5)
    return img[victimPos]

def champRecognition(img):
    cList = ['ahri','corki']
    for c in cList:
        lImg = cv2.imread((c + '.jpg'),0)
        lImg = cv2.resize(lImg,(len(img),len(img)),interpolation = cv2.INTER_AREA)
        score, diff = structural_similarity(img,lImg, full=True)
        if score > 0.4:
            return False
    return True
def getVictimChamp(victimPos):
    img = victimsImage(victimPos)
    img = circleDetect(img)
    shouldHurt = champRecognition(img)
    print(shouldHurt)
    if shouldHurt:
        taserTime.hurt(1.5)

from time import sleep

p = positionList()
while True:
    #sleep(1)
    getVictimChamp(p)
