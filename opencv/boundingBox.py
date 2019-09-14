# This janky goodness is proudly brought to you by the Glowfish crew at HackMIT 2019
# Tim, Zach, Luke, and Fischer have put some spice into this and we hope you enjoy it :)

import cv2 as cv
import numpy as np


#define the colors of the sticky notes, formatted as BGR (not RGB!)
white = np.array([255, 255, 255])
orange = np.array([50, 172, 244])
yellow = np.array([80, 227, 239]) 
pink = np.array([170, 143, 237])
blue = np.array([202, 198, 117])

image = cv.imread("Box_noSticky.jpg")

def findRectangles(image, color, lowTolerance, highTolerance):
    lower = np.full((1,3), -lowTolerance)
    upper = np.full((1,3), highTolerance)

    lower_mask = np.add(color, lower)
    upper_mask = np.add(color, upper)
    shapeMask = cv.inRange(image, lower_mask, upper_mask)
    return shapeMask

shapeMask = findRectangles(image, white, 50, 0)
cv.imshow("obj shapeMask", shapeMask)
cv.waitKey(0)

cnts = cv.findContours(shapeMask.copy(), cv.RETR_EXTERNAL,
                       cv.CHAIN_APPROX_SIMPLE)[0]

print(cnts)
print(type(cnts))

for c in cnts:
    peri = cv.arcLength(c, True)
    approx = cv.approxPolyDP(c, 0.04 * peri, True)
    if len(approx) == 4:
        (x, y, w, h) = cv.boundingRect(approx)
        cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), thickness=5)

        print("w:%s, y:%s, w:%s, h:%s" % (x, y, w, h))

        el = shapeMask.copy()[y:y + h, x:x + w]
        #pil_im = Image.fromarray(el)

        cv.imshow("obj", el)
        cv.waitKey(0)

        print(pytesseract.image_to_string(pil_im))


cv.imshow("obj rectangle", image)
cv.waitKey(0)