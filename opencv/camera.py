import cv2

def takePicture()
    camera = cv2.VideoCapture(0)
    image = camera.read()
    del(camera)
    return image
