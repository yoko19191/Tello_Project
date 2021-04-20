import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar  # sudo apt install libzbar0

path = "resource/HELLO_WORLD.png"

image = cv2.imread(path)

decodeObjects = pyzbar.decode(image)
for obj in decodeObjects:
    print("Type:", obj.type)
    print("Data:", obj.data, "\n")

