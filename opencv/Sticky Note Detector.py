#importing Modules
import cv2
import numpy as np

cam = cv2.VideoCapture(0)
while True:
    ret_val, img = cam.read()
    if mirror: 
        img = cv2.flip(img, 1)
    cv2.imshow('my webcam', img)
    if cv2.waitKey(1) == 27: 
        break  # esc to quit
    cv2.destroyAllWindows()