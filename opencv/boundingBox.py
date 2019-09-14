# This janky goodness is proudly brought to you by the Glowfish crew at HackMIT 2019
# Tim, Zach, Luke, and Fischer have put some spice into this and we hope you enjoy it :)

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial import distance as dist


#define the colors of the sticky notes, formatted as BGR (not RGB!)
white = np.array([255, 255, 255])
red = np.array([81, 110, 214])
orange = np.array([50, 172, 244])
yellow = np.array([80, 227, 239]) 
pink = np.array([170, 143, 237])
blue = np.array([202, 198, 117])

image = cv.imread("training/LessGay.jpg")

def maskByColor(image, color, lowTolerance, highTolerance):
    lower = np.full((1,3), -lowTolerance)
    upper = np.full((1,3), highTolerance)

    lower_mask = np.add(color, lower)
    upper_mask = np.add(color, upper)
    shapeMask = cv.inRange(image, lower_mask, upper_mask)
    return shapeMask

def generatePoints(image, color, lowTolerance, highTolerance):
    shapeMask = maskByColor(image, color, lowTolerance, highTolerance)
    cnts, _ = cv.findContours(shapeMask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    peri = cv.arcLength(cnts[0], True)
    approx = cv.approxPolyDP(cnts[0], 0.04 * peri, True)
    return approx

def order_points(pts):
	# sort the points based on their x-coordinates
	xSorted = pts[np.argsort(pts[:, 0]), :]
 
	# grab the left-most and right-most points from the sorted
	# x-roodinate points
	leftMost = xSorted[:2, :]
	rightMost = xSorted[2:, :]
 
	# now, sort the left-most coordinates according to their
	# y-coordinates so we can grab the top-left and bottom-left
	# points, respectively
	leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
	(tl, bl) = leftMost
 
	# now that we have the top-left coordinate, use it as an
	# anchor to calculate the Euclidean distance between the
	# top-left and right-most points; by the Pythagorean
	# theorem, the point with the largest distance will be
	# our bottom-right point
	D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
	(br, tr) = rightMost[np.argsort(D)[::-1], :]
 
	# return the coordinates in top-left, top-right,
	# bottom-right, and bottom-left order
	return np.array([tl, tr, br, bl], dtype="float32")

approx = generatePoints(image, red, 90, 35)
approx_trimmed = np.float32([x[0] for x in approx])

pts1 = order_points(approx_trimmed)
pts2 = np.float32([[0,0],[300,0],[300,300],[0,300]])

transform_matrix = cv.getPerspectiveTransform(pts1, pts2)

#generate transformed image
image_transformed = cv.warpPerspective(image, transform_matrix, (300,300))
image2 = cv.imread("training/sticky.jpg")

image2_transformed = cv.warpPerspective(image2, transform_matrix, (300, 300))


#plt.subplot(121),plt.imshow(image),plt.title('image')
#plt.subplot(122),plt.imshow(image_transformed),plt.title('image_transformed')
plt.subplot(121),plt.imshow(image2),plt.title('image2')
plt.subplot(122),plt.imshow(image2_transformed),plt.title('image2_transformed')
plt.show()