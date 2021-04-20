from djitellopy import Tello
from pyzbar.pyzbar import decode
import cv2
import numpy as np

tello = Tello()
tello.connect()
print("BATTERY:", tello.get_battery())

'''
Response tello command with input string
@:param cmd : command in string
'''

def getCodeInput(cmd):
    print("QR_CMD", cmd)
    while True:
        if cmd == "MOVE_LEFT":
            tello.move_left(30)
        elif cmd == "MOVE_RIGHT":
            tello.move_right(30)
        if cmd == "MOVE_FORWARD":
            tello.move_forward(30)
        elif cmd == "MOVE_BACK":
            tello.move_back(30)
        if cmd == "MOVE_UP":
            tello.move_up(30)
        elif cmd == "MOVE_DOWN":
            tello.move_down(30)
        if cmd == "ROTATE_COUNTER_CLOCKWISE":
            tello.rotate_counter_clockwise(90)
        elif cmd == "ROTATE_CLOCKWISE":
            tello.rotate_clockwise(90)
        if cmd == "LAND":
            tello.land()
        if cmd == "TAKE_OFF":
            tello.takeoff()


if __name__ == "__main__":
    # enable tello stream
    tello.streamon()
    # command and count initialization
    cmd = "NULL"
    count = 0

    while True:
        level = tello.get_battery()
        img = tello.get_frame_read().frame
        img = cv2.resize(img, (360, 240))
        # resolve every qr code from image
        for barcode in decode(img):
            data = barcode.data.decode('utf-8')
            # save decode result in qr_cmd
            cmd = data
            count = count + 1
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (255, 0, 255), 5)
            pts2 = barcode.rect
            cv2.putText(img, data, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (255, 0, 255), 2)
        cv2.putText(img, str(level), (10, 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
        cv2.imshow("Tello", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            tello.land()
            break
        # response cmd
        if count > 30:
            getCodeInput(cmd)
            qr_count = 0
            qr_cmd = "NULL"
