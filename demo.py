# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math
from face_detector import get_face_detector, find_faces
from face_landmarks import get_landmark_model, detect_marks,draw_marks
from head_pose_estimation import head_pose_points

face_model = get_face_detector()
landmark_model = get_landmark_model()
cap = cv2.VideoCapture(0)
#ret,img=cap.read()
#size = img.shape
font = cv2.FONT_HERSHEY_SIMPLEX 
outer_points = [[49, 59], [50, 58], [51, 57], [52, 56], [53, 55]]
d_outer = [0]*5
inner_points = [[61, 67], [62, 66], [63, 65]]
d_inner = [0]*3
while(True):
    ret, img = cap.read()
    size=img.shape
    rects = find_faces(img, face_model)
    for rect in rects:
        shapes = detect_marks(img, landmark_model, rect)
        #draw_marks(img,shapes)
        cv2.putText(img, 'Press r to record Mouth distances', (30, 30), font,
                    1, (0, 255, 255), 2)
        cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xFF == ord('r'):
        for i in range(100):
            for i, (p1, p2) in enumerate(outer_points):
                d_outer[i] += shapes[p2][1] - shapes[p1][1]
            for i, (p1, p2) in enumerate(inner_points):
                d_inner[i] += shapes[p2][1] - shapes[p1][1]
        break
cv2.destroyAllWindows()
cap.release()