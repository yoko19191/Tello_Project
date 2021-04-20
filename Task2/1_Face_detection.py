"""
todo
    run the example code provided by instructors to be able to detect faces in still images using Haar cascades
"""

import numpy as np
import cv2

# import weight file
face_cascade = cv2.CascadeClassifier('resource/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('resource/haarcascade_eye.xml')

# read local image
img = cv2.imread('resource/I_am_a_big_boy.jpg')
# convert RGB into gray_scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# call opencv api and save results in faces
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

# draw faces on image
for (x, y, w, h) in faces:
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    roi_gray = gray[y:y + h, x:x + w]
    roi_color = img[y:y + h, x:x + w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

# present image
cv2.namedWindow("face_detection", 0)
cv2.resizeWindow("face_detection", 640, 480)
cv2.imshow('face_detection', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
