"""
todo:
    1. design and print more QR codes if needed
    2. Take several images at known distances from the QR codes
    3. Calibrate a function that calculates the distance
       to the QR code based on its size in pixels in the image(assume parallel)
    4. Calculate the relative position to the QR code based on its size
       in pixels and its position within the image
    5. *Improve the position detection taking into account
       that the code might be seen from a non-perpendicular perspective
"""
from utlis import *
import cv2


# frame size
w, h = 360, 250
# PID param kp ki kd
pid= [0.5, 0.5, 0]
# previous Error : yaw_error, up_down_error, for_back_error
pError = [0, 0, 0]


if __name__ == "__main__":
    # tello initialization
    tello = initializeTello()

    while True:
        # Get frame
        img = getTelloFrame(tello, w, h)
        # decode qr code
        img, pts, data = decode(img)
        # measure distance
        distance = measureDistance(pts[2] * pts[3])

        print(distance)

        cv2.imshow("img", img)
        cv2.waitKey(1)
