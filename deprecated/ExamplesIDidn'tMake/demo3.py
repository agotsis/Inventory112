# demo3.py
# Alex Gotsis 3-8-16
# from https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_image_display/py_image_display.html

import numpy as np
import cv2

img = cv2.imread('bin/Lenna.png', cv2.IMREAD_GRAYSCALE)
cv2.imshow('Grey Lenna',img)

k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite('bin/LennaGray.png',img)
    cv2.destroyAllWindows()