import numpy as np
import cv2
import serial
import time
from networktables import NetworkTable

cap = cv2.VideoCapture(1)
port = "COM3"
baud = 9600

#ser = serial.Serial(port, baud, timeout=1)
# open the serial port
#if ser.isOpen():
 #   print(ser.name + ' is open...')

NetworkTable.initialize("10.18.16.2")

sd = NetworkTable.getTable("SmartDashboard")

min_area = 0.0
min_perimeter = 0.0
min_width = 0.0
max_width = 1000.0
min_height = 100.0
max_height = 1000.0
solidity = [0, 100]
max_vertices = 1000000.0
min_vertices = 0.0
min_ratio = 0.0
max_ratio = 1.0

# Color values - currently set to green vision tape
lower_color = np.array([15, 0, 234])
upper_color = np.array([100, 77, 255])

stagedX = []
stagedY = []
stagedArea = []

while True:
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of color in HSV
    mask = cv2.inRange(hsv, lower_color, upper_color)

    cv2.imshow('Mask', mask)

    k = cv2.waitKey(5) & 0xFF

    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    ncontours = []
    for contour in contours:
        if cv2.contourArea(contour) > 400:
            ncontours.append(contour)

    #print "Number of contours: ", len(ncontours)
    cX = []
    cY = []
    cArea = []
    # loop over the contours
    for c in ncontours:

        # Draw the contour and show it
        cv2.drawContours(frame, ncontours, -1, (0, 255, 0), 1)

        # Draw the bounding rectangle
        rect = cv2.boundingRect(c)
        x, y, w, h = cv2.boundingRect(c)

        if (h < min_height or h > max_height):
            continue

        ratio = (float)(w) / h
        if (ratio < min_ratio or ratio > max_ratio):
            continue
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Draw center of rectangle
        M = cv2.moments(c)
        cX.append(int(M["m10"] / M["m00"]))
        cY.append(int(M["m01"] / M["m00"]))
        cArea.append(int(M['m00']))
        #cv2.circle(frame, (int(cX), int(cY)), 7, (255, 255, 255), -1)

        print "Center: ", cX, cY

    sd.putNumberArray('X', cX)
    sd.putNumberArray('Y', cY)
    sd.putNumberArray('Area', cArea)

    cv2.imshow('Contour Window', frame)

ser.close()

cv2.destroyAllWindows()