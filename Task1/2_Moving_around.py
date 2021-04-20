"""
todo
    write a short code to command the drone into moving following a 2*2m square (approximately based on flight time at constant speed).
"""
from djitellopy import Tello

# create drone instance and connect
tello = Tello()
tello.connect()
print("BATTERY:", tello.get_battery())

# drone speed set to 20cm/s
tello.set_speed(20)

# drone taking off
tello.takeoff()

# drone moving up for 50cm
tello.move_up(50)

# forward 100cm and back origin pos
tello.move_forward(100)
tello.move_back(100)

# left 100cm and back
tello.move_left(100)
tello.move_right(100)

# backward 100cm and back
tello.move_back(100)
tello.move_forward(100)

# right 100cm and back
tello.move_right(100)
tello.move_left(100)

# drone landing
tello.land()
