from djitellopy import Tello
from threading import Thread
import time

# Create drone instance and connect
tello = Tello()
tello.connect()
# print current battery level
print("BATTERY:", tello.get_battery())

while True:
    print("-----------")
    print("BAROMETER: ", tello.get_barometer())
    print("DISTANCE: ", tello.get_distance_tof())
    print("ACCELERATION_X", tello.get_acceleration_x())
    print("ACCELERATION_Y", tello.get_acceleration_y())
    print("ACCELERATION_Z", tello.get_acceleration_z())
    print("SPEED_X", tello.get_speed_x())
    print("SPEED_Y", tello.get_speed_y())
    print("SPEED_Z", tello.get_speed_z())
    print("YAW:", tello.get_yaw())
    print("-----------")
    time.sleep(5)
