import cv2

def takePicture(name)
    camera = cv2.VideoCapture(0)
    image = camera.read()
    del(camera)
    return image
