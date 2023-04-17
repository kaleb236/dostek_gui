# import cv2
# import numpy as np

# cap = cv2.VideoCapture(0)

# while True:
#     ret, img = cap.read()
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     ret,thresh = cv2.threshold(gray,50,255,0)
#     edge = cv2.Canny(gray, 30, 200)
#     contours,hierarchy = cv2.findContours(edge, 1, 2)
#     print("Number of contours detected:", len(contours))

#     for cnt in contours:
#         x1,y1 = cnt[0][0]
#         approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
#         if len(approx) == 4:
#             x, y, w, h = cv2.boundingRect(cnt)
#             ratio = float(w)/h
#             if ratio >= 0.9 and ratio <= 1.1:
#                 img = cv2.drawContours(img, [cnt], -1, (0,255,255), 3)
#                 cv2.putText(img, 'Square', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
#             else:
#                 cv2.putText(img, 'Rectangle', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
#                 img = cv2.drawContours(img, [cnt], -1, (0,255,0), 3)

#     cv2.imshow("Shapes", img)
#     cv2.waitKey(1)
#     # cv2.destroyAllWindows()

import numpy as np
import cv2
video_capture = cv2.VideoCapture(0)
video_capture.set(3, 160)
video_capture.set(4, 120)
while(True):
    # Capture the frames
    ret, frame = video_capture.read()
    # Crop the image
    crop_img = frame[60:120, 0:160]
     # Convert to grayscale

    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    # Gaussian blur

    blur = cv2.GaussianBlur(gray,(5,5),0)

    # Color thresholding
    ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
    # Find the contours of the frame
    contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
    # Find the biggest contour (if detected)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        cx = int(M['m10']/M['m00'])

        cy = int(M['m01']/M['m00'])

        cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)

        cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)


        cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)

        if cx >= 120:

            print("Turn Left!")
        if cx < 120 and cx > 50:

            print("On Track!")

        if cx <= 50:
            print("Turn Right")
    else:
        print("I don't see the line")

    #Display the resulting frame

    cv2.imshow('frame',crop_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break