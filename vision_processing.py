import numpy as np
import cv2

cap = cv2.VideoCapture(0)

# Color values - currently set to green vision tape
lower_color = np.array([45, 0, 241])
upper_color = np.array([49, 37, 255])

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

    # loop over the contours
    for c in ncontours:

        # Draw the contour and show it
        cv2.drawContours(frame, ncontours, -1, (0, 255, 0), 1)

        # Draw the bounding rectangle
        rect = cv2.boundingRect(c)
        x, y, w, h = cv2.boundingRect(c)
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Draw center of rectangle
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
        print "Center: ", cX, cY

    cv2.imshow('Contour Window', frame)

cv2.destroyAllWindows()