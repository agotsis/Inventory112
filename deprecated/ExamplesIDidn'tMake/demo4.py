# demo3.py
# Alex Gotsis 3-8-16
# doesn't work!

import numpy as np
import cv2
from matplotlib import pyplot as plt


img = cv2.imread('bin/Leona.png', cv2.IMREAD_GRAYSCALE)
plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()