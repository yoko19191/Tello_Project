from djitellopy import Tello
import pyzbar.pyzbar as pyzbar
import cv2
import numpy as np

'''
Initialize tello drone 
    1. create and connect Tello Drone 
    2. enable video streaming
    3. set velocity to zero
    4. print current battery level
    5. return drone instance 
'''


def initializeTello():
    tello = Tello()
    tello.connect()
    tello.for_back_velocity = 0
    tello.left_right_velocity = 0
    tello.up_down_velocity = 0
    tello.yaw_velocity = 0
    tello.speed = 0
    print("BATTERY:", tello.get_battery());
    tello.streamoff()
    tello.streamon()
    return tello


'''
Get Tello Drone Frame
    @param tello : drone instance 
    @param w : width of frame
    @param h : height of frame 
'''


def getTelloFrame(tello, w=360, h=240):
    frame = tello.get_frame_read().frame
    img = cv2.resize(frame, (w, h))
    level = tello.get_battery()
    cv2.putText(img, str(level), (10, 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)

    return img


'''
decode QR_code with pyzbar
    @param img : input image
    return img, qr_code position info
'''


def decode(img):
    pts2 = [0, 0, 0, 0]
    for barcode in pyzbar.decode(img):
        data = barcode.data.decode('utf-8')
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, (255, 0, 255), 3)
        pts2 = barcode.rect
        cv2.putText(img, data, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (255, 0, 255), 2)

    # if QR_Code exits
    if pts2[0] != 0 and pts2[1] != 0:
        return img, pts2
    else:
        return img, [0, 0, 0, 0]


'''
PID Control drone at relative position 
    @param tello : drone instance 
    @param pts : qr code position 
    @param fw : width of frame
    @param fh : height of frame
    @param PID : PID control parameter (kp, kd, ki)
    @param pError : previous error
'''


def trackQRCode(tello, pts, fw, fh, pid, pError):
    # calculate error
    yaw_error = pts[0] - fw // 2
    up_down_error = pts[1] - fh // 2
    for_back_error = pts[2] * pts[3] - 83 * 79

    # PID control Speed
    yaw_speed = pid[0] * yaw_error + pid[1] * (yaw_error-pError[0])
    up_down_speed = pid[0] * up_down_error + pid[1] * (up_down_error-pError[1])
    for_back_speed = pid[0] * for_back_error + pid[1] * (for_back_error-pError[2])

    # if QR code exits
    if pts[0] != 0 and pts[1] != 0:
        tello.yaw_velocity = yaw_speed
        tello.up_down_velocity = up_down_speed
        tello.for_back_velocity = for_back_speed
    else:
        tello.yaw_velocity = 0
        tello.left_right_velocity = 0
        tello.up_down_velocity = 0
        tello.yaw_velocity = 0
        yaw_error = 0
        up_down_error = 0
        for_back_error = 0

    if tello.send_rc_control:
        tello.send_rc_control(tello.left_right_velocity,
                              tello.for_back_velocity,
                              tello.up_down_velocity,
                              tello.yaw_velocity)

    return [yaw_error, up_down_error, for_back_error]