import cv2

camera = cv2.VideoCapture(1)
image = camera.read()

file = "test_image.png"

cv2.imwrite(file, image)

del(camera)

