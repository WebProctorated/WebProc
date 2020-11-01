import cv2 as cv
import time
import numpy as np

vid = cv.VideoCapture(0)
face = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
arr = list()

while(True):
    ret, frame = vid.read()
    if(ret):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = face.detectMultiScale(gray, 1.1, 4)
        print(len(faces))

        arr.append(len(faces))
        cv.imshow('Student Frame', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break


vid.release()
cv.destroyAllWindows()
