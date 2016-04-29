# demo2.py
# Alex Gotsis 3-8-16
# from https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_image_display/py_image_display.html
import cv2

img1 = cv2.imread('bin/Lenna.png', cv2.IMREAD_COLOR)
img2 = cv2.imread('bin/ChromeLogo.png', cv2.IMREAD_COLOR)
img3 = cv2.imread('bin/ChromeLogo.png', cv2.IMREAD_GRAYSCALE)
img4 = cv2.imread('bin/ChromeLogo.png', cv2.IMREAD_UNCHANGED )

cv2.namedWindow('This is a picture of Lenna.', cv2.WINDOW_NORMAL)

cv2.namedWindow('This is a Chrome Color', cv2.WINDOW_NORMAL)


cv2.imshow('This is a picture of Lenna.', img1)
cv2.imshow('This is a Chrome Color', img2)
cv2.imshow('This is a Chrome Grey', img3)
cv2.imshow('This is a Chrome Alpha', img4)

cv2.waitKey(0)
cv2.destroyAllWindows()