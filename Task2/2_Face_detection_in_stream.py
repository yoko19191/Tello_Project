"""
todo
    merge your face detection code with the tello control code
    so that you can detect faces from the Tello camera stream in real time
"""
from djitellopy import Tello
from time import sleep
from Task2.resource import KeyPressModule as kp
import cv2
from threading import Thread

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
        # Csleep(3)
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
    # import weight file
    face_cascade = cv2.CascadeClassifier('resource/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('resource/haarcascade_eye.xml')
    # get video stream
    while True:
        level = tello.get_battery()
        img = tello.get_frame_read().frame
        img = cv2.resize(img, (360, 240))
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
        cv2.putText(img, str(level), (10, 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
        cv2.imshow("Tello_Face_Detection", img)
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