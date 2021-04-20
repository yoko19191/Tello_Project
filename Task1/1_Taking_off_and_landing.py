"""
todo
    write a short code to command the drone to hover in the air a few seconds and then land
"""

from djitellopy import Tello
from time import sleep

# Create drone instance and connect
tello = Tello()
tello.connect()

# print current battery level
print("BATTERY:", tello.get_battery())

# tello taking off
tello.takeoff()

# sleep for 3 seconds
sleep(3)

# tello landing
tello.land()
