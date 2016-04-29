# CVVideoDemo.py
# Alexander Gotsis + agotsis + EE

import numpy as np
import cv2

def openCamera(camIndex=0): # Default is 0.
    capture = cv2.VideoCapture(camIndex)
    capture.open(camIndex)

    while True:
        ret, frame = capture.read()

        if frame is not None:
            frame = processFrame(frame)
            cv2.imshow('Camera!', frame)

        k = cv2.waitKey(1) & 0xFF

        if k == 27:
            capture.release()
            cv2.destroyAllWindows()
            break

def processFrame(frame):
    grey = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(grey,(7,7),0)

    #ret, thresh = cv2.threshold(blur,100,255,cv2.THRESH_BINARY)
    thresh = cv2.Canny(blur, 70, 180)

    minArea = 20
    minHeight = 15

    image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour)>minArea:
            [x,y,w,h] = cv2.boundingRect(contour)
            if  h>minHeight:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

    return frame

openCamera()