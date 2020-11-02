import cv2 as cv
import numpy as np


phone_cascade = cv.CascadeClassifier('Phone_Cascade.xml')
camera = cv.VideoCapture(0, cv.CAP_DSHOW)

i = 0

while True:
    ret, frame = camera.read()
    cv.imshow('frame', frame)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # phones is basically the list of tuples containing rectangular coordinates of the phones detected
    phones = phone_cascade.detectMultiScale(gray, 3, 9)

    if len(phones) > 0:
        i += 1
        print("yes {}".format(i))

    key = cv.waitKey(1)
    if key == ord('q'):
        break

camera.release()
cv.destroyAllWindows()
