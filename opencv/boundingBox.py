# This janky goodness is proudly brought to you by the Glowfish crew at HackMIT 2019
# Tim, Zach, Luke, and Fischer have put some spice into this and we hope you enjoy it :)

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial import distance as dist
import os

#define the colors of the sticky notes, formatted as BGR (not RGB!)
white = np.array([255, 255, 255])
red = np.array([81, 110, 214])

orange = np.array([50, 130, 183])
green = np.array([73, 138, 125])
pink = np.array([113, 60, 201])
blue = np.array([195, 160, 126])

def takePicture():
    camera = cv.VideoCapture(0)
    image = camera.read()
    del(camera)
    return image

def maskByColor(image, color, lowTolerance, highTolerance):
	lower = np.full((1,3), -lowTolerance)
	upper = np.full((1,3), highTolerance)

	lower_mask = np.add(color, lower)
	upper_mask = np.add(color, upper)
	shapeMask = cv.inRange(image, lower_mask, upper_mask)
	return shapeMask

def generatePoints(image, color, lowTolerance, highTolerance):
	shapeMask = maskByColor(image, color, lowTolerance, highTolerance)
	contours, _ = cv.findContours(shapeMask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

	#find the largest contour and use that one!
	largest_contour = contours[0]
	for contour in contours:
		if cv.contourArea(contour) > cv.contourArea(largest_contour):
			largest_contour = contour

	peri = cv.arcLength(largest_contour, True)
	approx = cv.approxPolyDP(largest_contour, 0.04 * peri, True)
	return approx

def generateFilteredContourList(shapeMask, minContourArea):
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

def genCalTransformMatrix(image, color, lowTolerance, highTolerance, width, height):
	approx = generatePoints(image, color, lowTolerance, highTolerance)
	approx_trimmed = np.float32([x[0] for x in approx])

	pts1 = order_points(approx_trimmed)
	pts2 = np.float32([[0,0],[width,0],[width,height],[0,height]])

	transform_matrix = cv.getPerspectiveTransform(pts1, pts2)
	return transform_matrix

def lookForColor(image, transform_matrix, color, colorName, lowTolerance, highTolerance, grid_width, grid_height):
	color_mask = maskByColor(image, color, lowTolerance, highTolerance)
	contour_list = generateFilteredContourList(color_mask, 100) #the 100 is the general size of the sticky note, but this number is largely emperical
	image_redrawn = image.copy()

	bounding_box_coords = []
	for contour in contour_list:
		x, y, w, h = cv.boundingRect(contour)
		formatted_tuple = (x, y, w, h, colorName)
		bounding_box_coords.append(formatted_tuple)

		b, g, r = tuple(color)
		b = int(b)
		g = int(g)
		r = int(r)
		cv.rectangle(image_redrawn, (x,y), (x + w, y + h), (b, g, r), 2)
	
	return bounding_box_coords, image_redrawn.copy()
				
def lookForGreen(image, transform_matrix, grid_width, grid_height):
	return lookForColor(image, transform_matrix, green, "green", 20, 25, grid_width, grid_height)

def lookForOrange(image, transform_matrix, grid_width, grid_height):
	return lookForColor(image, transform_matrix, orange, "orange", 20, 25, grid_width, grid_height)

def lookForPink(image, transform_matrix, grid_width, grid_height):
	return lookForColor(image, transform_matrix, pink, "pink", 40, 45, grid_width, grid_height)

def lookForBlue(image, transform_matrix, grid_width, grid_height):
	return lookForColor(image, transform_matrix, blue, "blue", 35, 40, grid_width, grid_height)

def calibrateFromCamera():
	camera = cv2.VideoCapture(1)
	image = camera.read()
	del(camera)

	if(os.path.exists("currentCalib.jpg")):
		os.remove("currentCalib.jpg")
	cv.imwrite("currentCalib.jpg", image)

	return genCalTransformMatrix(image, red, 90, 80, grid_width, grid_height)

def updateFromCamera():
	camera = cv2.VideoCapture(1)
	image = camera.read()
	del(camera)

	if(os.path.exists("currentBoard.jpg")):
		os.remove("currentBoard.jpg")
	cv.imwrite("currentBoard.jpg", image)

	bounding_box_coords = []
	green_coords, green_painted = lookForGreen(image, transform_matrix, grid_width, grid_height)
	orange_coords, orange_painted = lookForOrange(image, transform_matrix, grid_width, grid_height)
	pink_coords, pink_painted = lookForPink(image, transform_matrix, grid_width, grid_height)
	blue_coords, blue_painted = lookForBlue(image, transform_matrix, grid_width, grid_height)

	bounding_box_coords.append(green_coords)
	bounding_box_coords.append(orange_coords)
	bounding_box_coords.append(pink_coords)
	bounding_box_coords.append(blue_coords)
	print(bounding_box_coords)


cal_image = cv.imread("training/redCalibration2.jpg")
cal_mask = maskByColor(cal_image, red, 90, 80)

cv.imshow("calib", cal_mask)
cv.waitKey()

grid_width = 400
grid_height = 300
transform_matrix = genCalTransformMatrix(cal_image, red, 90, 80, grid_width, grid_height)

#generate transformed image
image = cv.imread("training/sticky2.jpg")
image_transformed = cv.warpPerspective(image, transform_matrix, (grid_width, grid_height))


bounding_box_coords = []
green_coords, green_painted = lookForGreen(image_transformed, transform_matrix, grid_width, grid_height)
orange_coords, orange_painted = lookForOrange(image_transformed, transform_matrix, grid_width, grid_height)
pink_coords, pink_painted = lookForPink(image_transformed, transform_matrix, grid_width, grid_height)
blue_coords, blue_painted = lookForBlue(image_transformed, transform_matrix, grid_width, grid_height)

bounding_box_coords.append(green_coords)
bounding_box_coords.append(orange_coords)
bounding_box_coords.append(pink_coords)
bounding_box_coords.append(blue_coords)
print(bounding_box_coords)


cv.imshow("green", green_painted)
cv.imshow("orange", orange_painted)
cv.imshow("pink", pink_painted)
cv.imshow("blue", blue_painted)

plt.subplot(121),plt.imshow(image),plt.title('image')
plt.subplot(122),plt.imshow(image_transformed),plt.title('image_transformed')
plt.show()