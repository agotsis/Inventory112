# CVBasicContour.py
# Alexander Gotsis + agotsis + EE

#version for simple contour finding on image, showing process

import numpy as np
import cv2

original = cv2.imread('bin/TooEasy.png')
im = original.copy()

gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)
thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)

minArea = 30
minHeight = 20

# find contours!

image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,
    cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    if cv2.contourArea(contour)>minArea:
        [x,y,w,h] = cv2.boundingRect(contour)
        if  h>minHeight:
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.imshow('norm',im)

key = cv2.waitKey(0)
cv2.destroyAllWindows()