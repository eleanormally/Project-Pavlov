from PIL import ImageGrab as imgg
import win32ui as win
import win32gui as wig
import cv2
import numpy as np
from PIL import Image

def process(img):
    #basic image processing
        #monochromeify (not a word but I don't care)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
        #increase contrast
    img = (img-0.5)*2 + 0.5
        #thiccify (small letters don't work well for some reason even though they look exactly the same scaled up)
    img = cv2.resize(img, (0,0), fx=3, fy=3)
        #binarize
    ret,img = cv2.threshold(img,230,255,cv2.THRESH_BINARY)
    #trying to get rid of everything but the usernames (not perfect and needs ocr cleanup)
        #dilation (bold letters after making them thin)
    img = cv2.dilate(img,np.ones((2,3),np.uint8),iterations=1)
        #line erosion
    img = cv2.erode(img,np.ones((2,3),np.uint8),iterations=2)
    return img

def getImage(img=False):
    #read the function name dumbass
    appName = "League of Legends"
    try:
        coords = wig.GetWindowRect(win.FindWindow(None,appName).GetSafeHwnd())
    except:
        return False

    #get left of window
    coords = list(coords)
    coords[1] += coords[3]/12
    coords[2] /=2.7
    coords[0] += coords[2]/5
    coords[3] -= coords[3]/4
    if img:
        coords[0]/=1.15
        coords[1]+=20
        coords[3]+=20
        coords[2]-=140
    sc = imgg.grab(coords)
    if not img:
        sc = process(sc)
    else:
        sc = np.asarray(sc)
    return sc
