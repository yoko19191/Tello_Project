"""
todo
    write a short code to command the drone to slowly move around its original
    position (you may choose the path shape) and land whenever a face is detected for a few seconds.
"""

from djitellopy import Tello
from time import sleep
from Task2.resource import KeyPressModule as kp
import cv2
from threading import Thread

# kp.init()
# tello initialization
tello = Tello()
tello.connect()
print("BATTERY:", tello.get_battery())


# define video stream behavior
def stream():
    tello.streamon()
    # import weight file
    face_cascade = cv2.CascadeClassifier('resource/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('resource/haarcascade_eye.xml')
    # create landing flag [non-land 0, land 1]
    flag_land = 0
    # get video stream
    face_count = 0
    while True:
        level = tello.get_battery()
        img = tello.get_frame_read().frame
        img = cv2.resize(img, (360, 240))
        # convert RGB into gray_scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # call opencv api and save results in faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        # draw faces on image
        if len(faces) > 0:
            face_count = face_count + 1
            print("FACE_COUNT:", face_count)
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        cv2.putText(img, str(level), (10, 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
        cv2.imshow("Tello_Face_Detection", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            tello.land()
        # landing condition
        if face_count > 30:
            face_count = 0
            tello.land()



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
    # todo: slowly move around its original position
    tello.takeoff()
    tello.move_up(50)
    tello.move_forward(100)
    tello.rotate_clockwise(180)
    while True:
        ## Send Keyboard Control
        # vals = getKeyboardInput()
        # tello.send_rc_control(vals[0], vals[1], vals[2], vals[3])
        # lr, fb, ud, yw
        # tello.send_rc_control(30, -30, 0, 0)
        tello.move_left(100)
        tello.rotate_clockwise(90)
        tello.move_left(200)
        tello.rotate_clockwise(90)
        tello.move_left(200)
        tello.rotate_clockwise(90)
        tello.move_left(200)
        tello.rotate_clockwise(90)
        tello.move_left(100)


