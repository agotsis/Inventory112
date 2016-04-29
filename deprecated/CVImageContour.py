# CVImageContour.py
# Alexander Gotsis + agotsis + EE

#version for simple contour finding on image, showing process

import numpy as np
import cv2

screenWidth = 2560/2
screenHeight = 1600/2

#original = cv2.imread('bin/TooEasy.png')
original = cv2.imread('bin/View1.jpg')
copy = original.copy()

height, width = original.shape[:2] # or original.width, height

print(height, width)

scaleFactor = max(width/screenWidth, height/screenHeight)
print(scaleFactor)

if scaleFactor > 1:
    copy = cv2.resize(original,(int(width/scaleFactor), int(height/scaleFactor))
        , interpolation = cv2.INTER_AREA)

grey = cv2.cvtColor(copy,cv2.COLOR_BGR2GRAY)
cv2.imshow('Greyscale Image',grey)

key = cv2.waitKey(0)
cv2.destroyAllWindows()

blur = cv2.GaussianBlur(grey,(5,5),0)
cv2.imshow('Blurred Image',blur)

key = cv2.waitKey(0)
cv2.destroyAllWindows()

thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
cv2.imshow('Thresholded Image',thresh)

key = cv2.waitKey(0)
cv2.destroyAllWindows()

minArea = 20
minHeight = 15

image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,
    cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    if cv2.contourArea(contour)>minArea:
        [x,y,w,h] = cv2.boundingRect(contour)
        if  h>minHeight:
            cv2.rectangle(copy,(x,y),(x+w,y+h),(0,0,255),2)

cv2.imshow('Contoured Copy',copy)

key = cv2.waitKey(0)
cv2.destroyAllWindows()