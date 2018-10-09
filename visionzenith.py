import sys
import numpy as np
import cv2

# import serial

cap = cv2.VideoCapture(0)
#NetworkTables.initialize(server='10.18.16.2')
# port = "COM3"
# baud = 9600

# ser = serial.Serial(port, baud, timeout=1)
# open the serial port
# if ser.isOpen():
#     print(ser.name + ' is open...')


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

#table = NetworkTables.getTable("SmartDashboard")
#f table:
 #   print "table OK"
#table.putNumber("visionX", -1)
#table.putNumber("visionY", -1)

visionFlag = True
debugFlag = False
if len(sys.argv) > 1:
    visionFlag = sys.argv[1] == "-v" or sys.argv[2] == "-v"
    debugFlag = sys.argv[1] == "-d" or sys.argv[2] == "-d"
    print("Vision flag is: {};  debug flag: {}".format(visionFlag, debugFlag))


# Color values - currently set to green vision tape
lower_color = np.array([62.0, 100.0, 100.0])
upper_color = np.array([82.0, 255.0, 255.0])

while True:
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of color in HSV
    mask = cv2.inRange(hsv, lower_color, upper_color)

    if visionFlag:
        cv2.imshow('Mask', mask)

    k = cv2.waitKey(5) & 0xFF

    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    ncontours = []
    for contour in contours:
        if cv2.contourArea(contour) > 400:
            ncontours.append(contour)

    # print "Number of contours: ", len(ncontours)

    kX = 0
    tX = 0
    kY = 0
    tY = 0

    #loop over the contours
    for c in ncontours:

        # Draw the contour and show it
        cv2.drawContours(frame, ncontours, -1, (0, 255, 0), 1)

        # Draw the bounding rectangle
        rect = cv2.boundingRect(c)
        x, y, w, h = cv2.boundingRect(c)
        # print("xywh: {} {} {} {}".format(x,y,w,h))

        if (h < min_height or h > max_height):
            continue

        ratio = (float)(w) / h
        if (ratio < min_ratio or ratio > max_ratio):
            continue
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Draw center of rectangle
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
        #print("Center: {} {}".format( cX, cY))

        kX += cX
        kY += cY

        tX += 1
        tY += 1

    if tX > 0 and tY > 0:
        X = kX / tX
        Y = kY / tY
    else:
        X = -1
        Y = -1
        if debugFlag:
            print("tX or tY = 0")

    # #if len(ncontours) == 0:
    #     table.putNumber("visionX", -1)
    #     table.putNumber("visionY", -1)
    #     if debugFlag:
    #         print "TARGET NOT FOUND"
    # else:
    #     table.putNumber("visionX", X)
    #     table.putNumber("visionY", Y)
    #     if debugFlag:
    #         print "vision X, Y = {} {}".format(X, Y)

    # if ser.isOpen() == False:
    #     ser.open()
    #
    # ser.write(X + " " + Y)
    # ser.close()

    kX = 0;
    kY = 0;
    tX = 0;
    tY = 0;
    if visionFlag:
        cv2.imshow('Contour Window', frame)

cv2.destroyAllWindows()