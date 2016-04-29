# Basic webcam. I did not write this code.
import numpy as np
import cv2

def openCamera(camIndex=0): # Default is 0.
    capture = cv2.VideoCapture(camIndex)
    capture.open(camIndex)

    while True:
        ret, frame = capture.read()

        if frame is not None:
            greyFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #throwaway, display = cv2.threshold(greyFrame, 15, 255, 
                #cv2.THRESH_BINARY)
            display = cv2.Canny(greyFrame, 100, 200)
            cv2.imshow('Camera!', display)

        k = cv2.waitKey(1) & 0xFF

        if k == 27:
            capture.release()
            cv2.destroyAllWindows()
            break


openCamera()
quit()