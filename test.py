import cv2
import numpy as np

with open("img.png", "rb") as fp:
    data = fp.read()


# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
array = np.asarray(bytearray(data), dtype=np.uint8)
image = cv2.imdecode(array, cv2.IMREAD_COLOR)
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()