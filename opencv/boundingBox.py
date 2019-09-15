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
green = np.array([73, 138, 125])
pink = np.array([170, 143, 237])
blue = np.array([202, 198, 117])

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

def generateSortedContourList(shapeMask, minContourArea):
	#takes the list of contours that we generated, and filters out the ones that don't have enough area
	unfiltered_contour_list, _ = cv.findContours(shapeMask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
	filtered_contour_list = []

	for contour in unfiltered_contour_list:
		area = cv.contourArea(contour)
		if area >= minContourArea: filtered_contour_list.append(contour)

	return filtered_contour_list
		
		

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

def generateCalibrationTransformMatrix(image, color, lowTolerance, highTolerance, width, height):
    approx = generatePoints(image, color, lowTolerance, highTolerance)
    approx_trimmed = np.float32([x[0] for x in approx])

    pts1 = order_points(approx_trimmed)
    pts2 = np.float32([[0,0],[width,0],[width,height],[0,height]])

    transform_matrix = cv.getPerspectiveTransform(pts1, pts2)
    return transform_matrix


calImage = cv.imread("training/LessGay.jpg")
grid_width = 400
grid_height = 300
transform_matrix = generateCalibrationTransformMatrix(calImage, red, 90, 35, grid_width, grid_height)

#generate transformed image
image = cv.imread("training/green.jpg")
image_transformed = cv.warpPerspective(image, transform_matrix, (grid_width, grid_height))

greenMask = maskByColor(image_transformed, green, 20, 25)
cv.imshow("greenMask", greenMask)
contour_list = generateSortedContourList(greenMask, 100)
print(len(contour_list))

image_transformed_painted = image_transformed.copy()

bounding_box_coords = []
for contour in contour_list:
	color = "green"
	x, y, w, h = cv.boundingRect(contour)
	formatted_tuple = (x, y, w, h, color)

	cv.rectangle(image_transformed_painted,(x,y),(x+w,y+h),(0,255,0),3)
	bounding_box_coords.append(formatted_tuple)



print(bounding_box_coords)
	

cv.imshow("image_transformed_painted", image_transformed_painted)

plt.subplot(121),plt.imshow(image),plt.title('image')
plt.subplot(122),plt.imshow(image_transformed),plt.title('image_transformed')
plt.show()