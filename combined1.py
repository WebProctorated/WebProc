# -*- coding: utf-8 -*-

import cv2
import numpy as np
import pandas as pd
import math
from face_detector import get_face_detector, find_faces
from face_landmarks import get_landmark_model, detect_marks,draw_marks
from model import final_predictor
import matplotlib.pyplot as plt

def get_2d_points(img, rotation_vector, translation_vector, camera_matrix, val):
   
    point_3d = []
    dist_coeffs = np.zeros((4,1))
    rear_size = val[0]
    rear_depth = val[1]
    point_3d.append((-rear_size, -rear_size, rear_depth))
    point_3d.append((-rear_size, rear_size, rear_depth))
    point_3d.append((rear_size, rear_size, rear_depth))
    point_3d.append((rear_size, -rear_size, rear_depth))
    point_3d.append((-rear_size, -rear_size, rear_depth))
    
    front_size = val[2]
    front_depth = val[3]
    point_3d.append((-front_size, -front_size, front_depth))
    point_3d.append((-front_size, front_size, front_depth))
    point_3d.append((front_size, front_size, front_depth))
    point_3d.append((front_size, -front_size, front_depth))
    point_3d.append((-front_size, -front_size, front_depth))
    point_3d = np.array(point_3d, dtype=np.float).reshape(-1, 3)
    
    # Map to 2d img points
    (point_2d, _) = cv2.projectPoints(point_3d,
                                      rotation_vector,
                                      translation_vector,
                                      camera_matrix,
                                      dist_coeffs)
    point_2d = np.int32(point_2d.reshape(-1, 2))
    return point_2d
def head_pose_points(img, rotation_vector, translation_vector, camera_matrix):
    
    rear_size = 1
    rear_depth = 0
    front_size = img.shape[1]
    front_depth = front_size*2
    val = [rear_size, rear_depth, front_size, front_depth]
    point_2d = get_2d_points(img, rotation_vector, translation_vector, camera_matrix, val)
    y = (point_2d[5] + point_2d[8])//2
    x = point_2d[2]
    
    return (x, y)
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
face_count = []
ang_1 = []
ang_2 = []
mouth_outer_count = []
mouth_inner_count = []
phone_confidence = []
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
d_outer[:] = [x / 100 for x in d_outer]
d_inner[:] = [x / 100 for x in d_inner]
model_points = np.array([
                            (0.0, 0.0, 0.0),             # Nose tip
                            (0.0, -330.0, -65.0),        # Chin
                            (-225.0, 170.0, -135.0),     # Left eye left corner
                            (225.0, 170.0, -135.0),      # Right eye right corne
                            (-150.0, -150.0, -125.0),    # Left Mouth corner
                            (150.0, -150.0, -125.0)      # Right mouth corner
                        ])
focal_length = size[1]
center = (size[1]/2, size[0]/2)
camera_matrix = np.array(
                         [[focal_length, 0, center[0]],
                         [0, focal_length, center[1]],
                         [0, 0, 1]], dtype = "double"
                         )

thres = 0.45 # Threshold to detect object
classNames = ["cell phone"]
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'


net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

q=1
xvals=[]
yvals=[]
def animate(s,q):
    xvals.append(q)
    yvals.append(s)
while(True):
    ret, img = cap.read()
    rects = find_faces(img, face_model)
    nfaces=len(rects)
    if nfaces!=1:
        cv2.imshow("Output", img)
        print([nfaces,0,0,0,0,0])
        face_count.append(nfaces)
        ang_1.append(0)
        ang_2.append(0)
        mouth_outer_count.append(0)
        mouth_inner_count.append(0)
        phone_confidence.append(0)
        x=pd.DataFrame(np.array([nfaces,0,0,0,0,0]).reshape(1,-1))
        s=final_predictor(x)
        print(s)
        animate(s,q)
        q=q+1
#        ani=FuncAnimation(plt.gcf(),animate,interval=1)
        
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        for face in rects:
            marks = detect_marks(img, landmark_model, face)
                    # mark_detector.draw_marks(img, marks, color=(0, 255, 0))
            cnt_outer = 0
            cnt_inner = 0
            image_points = np.array([marks[30],     # Nose tip
                                     marks[8],     # Chin
                                     marks[36],     # Left eye left corner
                                     marks[45],     # Right eye right corne
                                     marks[48],     # Left Mouth corner
                                     marks[54]      # Right mouth corner
                                     ], dtype="double")
            dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
            (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_UPNP)
        
                    
            (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)

            p1 = ( int(image_points[0][0]), int(image_points[0][1]))
            p2 = ( int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
            x1, x2 = head_pose_points(img, rotation_vector, translation_vector, camera_matrix)
            classIds, confs, bbox = net.detect(img,confThreshold=thres)
    # print(classIds,confs,bbox)
            if len(classIds) != 0:
                for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
                    if classId == 77:
                        c=confidence
                    else:
                        c=0
            try:
                m = (p2[1] - p1[1])/(p2[0] - p1[0])
                ang1 = int(math.degrees(math.atan(m)))
                ang1=ang1/90
            except:
                ang1 = 90
                ang1=ang1/90
                
            try:
                m = (x2[1] - x1[1])/(x2[0] - x1[0])
                ang2 = int(math.degrees(math.atan(-1/m)))
                ang2=ang2/90
            except:
                ang2 = 90/90
            for i, (m1, m2) in enumerate(outer_points):
                if d_outer[i] + 3 < marks[m2][1] - marks[m1][1]:
                    cnt_outer += 1 
            cnt_outer=cnt_outer/5
            for i, (m1, m2) in enumerate(inner_points):
                if d_inner[i] + 2 <  marks[m2][1] - marks[m1][1]:
                    cnt_inner += 1
            cnt_inter=cnt_inner/3
            print([nfaces,ang1,ang2,cnt_outer,cnt_inner,c])
            x=pd.DataFrame(np.array([nfaces,ang1,ang2,cnt_outer,cnt_inner,c]).reshape(1,-1))
            #print(x)
            if cnt_outer >3 and cnt_inner >2:
                cv2.putText(img, 'Mouth open', (30, 30), font,
                    1, (0, 255, 255), 2)
        draw_marks(img,marks)
        cv2.imshow("Output", img)
        face_count.append(nfaces)
        ang_1.append(ang1)
        ang_2.append(ang2)
        mouth_outer_count.append(cnt_outer)
        mouth_inner_count.append(cnt_inner)
        phone_confidence.append(c)

        s=final_predictor(x)
        print(s)
        animate(s,q)
        q=q+1
#        ani=FuncAnimation(plt.gcf(),animate,interval=1000)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
plt.plot(xvals,yvals)
plt.show()
cv2.destroyAllWindows()
cap.release()
#df = pd.DataFrame({
#                    'no_faces':face_count,
#                    'Angle1':ang_1,
#                    'Angle2':ang_2,
#                    'cnt_inner':mouth_outer_count,
#                    'cnt_outer':mouth_inner_count,
#                    'Phone_detected':phone_confidence
#                })
#
#df.to_csv('class5.csv')


