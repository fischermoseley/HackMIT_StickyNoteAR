# This janky goodness is proudly brought to you by the Glowfish crew at HackMIT 2019
# Tim, Zach, Luke, and Fischer have put some spice into this and we hope you enjoy it :)

import cv2 as cv
import numpy as np

filename = "TestingImage.jpg"

#define the colors of the sticky notes, formatted as BGR (not RGB!)
orange = np.array([50, 172, 244])
yellow = np.array([80, 227, 239]) 
pink = np.array([170, 143, 237])
blue = np.array([202, 198, 117])


def findRectangles(filename, color, lowTolerance, highTolerance):
    lower = np.full((1,3), -lowTolerance)
    upper = np.full((1,3), highTolerance)
    image = cv.imread(filename)

    lower_mask = np.add(color, lower)
    upper_mask = np.add(color, upper)
    print(lower_mask)
    print(color)
    print(upper_mask)
    shapeMask = cv.inRange(image, lower_mask, upper_mask)
    return shapeMask

shapeMask = findRectangles("TestingImage.jpg", orange, 15, 15)
cv.imshow("obj shapeMask", shapeMask)
cv.waitKey(0)