#Progress Attempt

# Alex Gotsis + agotsis + EE + 3-8-16

import numpy as np
import cv2

def prepareForAnalysis(path):
    return cv2.imread(path, cv2.IMREAD_GRAYSCALE)

def run():
    imagePath = "bin/view1.jpg"
    fullImage = cv2.imread(imagePath, cv2.IMREAD_COLOR)
    print(type(fullImage))
    smallerImage = np.ndarray
    cv2.resize(fullImage, smallerImage, .5, .5)
    cv2.namedWindow('Image Test', cv2.WINDOW_NORMAL)
    cv2.imshow('Image Test', fullImage)

    while True:
        if cv2.waitKey(1) & 0xFF == 27:
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    run()