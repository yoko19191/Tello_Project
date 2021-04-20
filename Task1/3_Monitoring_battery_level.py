"""
todo
    write a short code that commands the drone to land if the battery level is below a threshold. Also print the
    battery level in the terminal when it drops in 5% steps
"""

import cv2
from djitellopy import Tello

# frame size
w, h = 360, 240

# create tello instance
tello = Tello()
tello.connect()
tello.streamon()
# print current battery level
print("BATTERY:", tello.get_battery())

# start counter [0, flight] [1, no flight]
startCounter = 0

# get video stream
while True:
    # take off at first time
    if startCounter == 0:
        tello.takeoff()
        startCounter = 1
    # Get stream frame and resize frame
    img = tello.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    # put battery level on each frame
    level = tello.get_battery()
    cv2.putText(img, str(level), (10, 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
    cv2.imshow("Tello", img)
    # wait frame loading and press 'q' to land
    if cv2.waitKey(1) & 0xFF == ord('q'):
        tello.land()
        break
