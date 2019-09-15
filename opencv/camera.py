import cv2

camera = cv2.VideoCapture(1)
image = camera.read()
cv2.imwrite('opencv'+str(i)+'.png', image)
del(camera)

