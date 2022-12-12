import cv2
import numpy as np
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
cam.set(cv2.CAP_PROP_EXPOSURE, -3)
cam.set(cv2.CAP_PROP_AUTO_WB, 0)


#blue
lower_blue = np.array([95, 70, 140])
upper_blue = np.array([105, 255, 255])

#green
lower_green = np.array([50, 20, 120])
upper_green = np.array([90, 120, 255])

#red
lower_red = np.array([170, 100, 90])
upper_red = np.array([255, 255, 255])


pixel = None
while cam.isOpened():
    _, frame = cam.read()
    frame = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_red = cv2.inRange(hsv, lower_red, upper_red)

    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

    
    if len(contours_blue) > 0:
        c = max(contours_blue, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(c)
        if radius > 20:
            cv2.circle(frame, (int(x), int(y)),int(radius),
                                (0, 255, 255, 0), 0)
            pixel = "Blue"

    if len(contours_green) > 0:
        c = max(contours_green, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(c)
        if radius > 20:
            cv2.circle(frame, (int(x), int(y)),int(radius),
                                (0, 255, 255, 0), 0)
            pixel = "Green"

    if len(contours_red) > 0:
        c = max(contours_red, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(c)
        if radius > 20:
            cv2.circle(frame, (int(x), int(y)),int(radius),
                                (0, 255, 255, 0), 0)
            pixel = "Red"


    cv2.putText(frame, f"HSV = {pixel}", (10, 30),
                cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 0))
    cv2.imshow("Image", frame)
    pixel = None 
    key = cv2.waitKey(50)
    if key == ord('q'):
        break
 
cv2.destroyAllWindows()