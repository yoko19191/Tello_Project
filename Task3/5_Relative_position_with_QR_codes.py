"""
todo:
     *control the drone autonomously to stay at a certain relative position to the QR codes
     PID control
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
    # Tello Initialization
    tello = initializeTello()

    while True:
        img = getTelloFrame(tello, w, h)
        img, pts = decode(img)

        # print("W:", pts[2], "H", pts[3]) # W,H = 83, 79 at 15cm => 6557

        pError = trackQRCode(tello, pts, w, h, pid, pError)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            tello.land()
            break
