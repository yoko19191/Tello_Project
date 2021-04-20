from djitellopy import Tello
from time import sleep
from Task3.resource import KeyPressModule as kp
from pyzbar.pyzbar import decode
import cv2
from threading import Thread
import numpy as np

kp.init()
tello = Tello()
tello.connect()
print("BATTERY:", tello.get_battery())

# define keyboard response
def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50
    if kp.getKey("LEFT"):
        lr = -speed
    elif kp.getKey("RIGHT"):
        lr = speed
    if kp.getKey("UP"):
        fb = speed
    elif kp.getKey("DOWN"):
        fb = -speed
    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed
    if kp.getKey("a"):
        yv = -speed
    elif kp.getKey("d"):
        yv = speed
    if kp.getKey("q"):
        tello.land()
        # sleep(3)
    if kp.getKey("e"):
        tello.takeoff()
    if kp.getKey("i"):
        tello.flip_forward()
    if kp.getKey("k"):
        tello.flip_back()
    if kp.getKey("j"):
        tello.flip_left()
    if kp.getKey("l"):
        tello.flip_right()

    return [lr, fb, ud, yv]


# define video stream behavior
def stream():
    tello.streamon()
    # get video stream
    while True:
        level = tello.get_battery()
        img = tello.get_frame_read().frame
        img = cv2.resize(img, (360, 240))
        for barcode in decode(img):
            result = barcode.data.decode('utf-8')
            print(result)
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (255, 0, 255), 5)
            pts2 = barcode.rect
            cv2.putText(img, result, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (255, 0, 255), 2)
        cv2.putText(img, str(level), (10, 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
        cv2.imshow("Tello", img)
        cv2.waitKey(1)



'''
Press E to take off, Q to landing
A and D control drone's yaw (clockwise or counter clockwise)
W and S control drone's up and down
Arrow UP and DOWN control drone's forward and backward
Arrow RIGHT and LEFT control drone's left and right
I, K, J, L doing flip
'''
if __name__ == "__main__":
    video_thread = Thread(target=stream)
    video_thread.start()
    while True:
        vals = getKeyboardInput()
        tello.send_rc_control(vals[0], vals[1], vals[2], vals[3])
        sleep(0.05)