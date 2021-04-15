import cv2
import time
import numpy as np
import pandas as pd
import math
from proctoring.face_detector import get_face_detector, find_faces
from proctoring.face_landmarks import get_landmark_model, detect_marks, draw_marks
from proctoring.model import final_predictor
import matplotlib.pyplot as plt
# import warnings
# warnings.filterwarnings('error')


class Proctor:
    def __init__(self):
        # capturing video
        self.video = cv2.VideoCapture(0)
        self.face_model = get_face_detector()
        self.landmark_model = get_landmark_model()
        self.outer_points = [[49, 59], [50, 58], [51, 57], [52, 56], [53, 55]]
        self.d_outer = [0]*5
        self.inner_points = [[61, 67], [62, 66], [63, 65]]
        self.d_inner = [0]*3
        self.face_count = []
        self.ang_1 = []
        self.ang_2 = []
        self.mouth_outer_count = []
        self.mouth_inner_count = []
        self.phone_confidence = []
        self.thres = 0.45  # Threshold to detect object
        self.classNames = ["cell phone"]
        self.configPath = './proctoring/models/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        self.weightsPath = './proctoring/models/frozen_inference_graph.pb'
        self.net = cv2.dnn_DetectionModel(self.weightsPath, self.configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0 / 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)
        self.orient = []
        self.q = 1
        self.xvals = np.array([])
        self.yvals = np.array([])
        self.base = 0
        self.STATE = 'CHECK_ROOM_INTENSITY'
        self.CHEAT = False
        self.TAB_CHANGE = False
        # np.seterr(all='raise')

    def __del__(self):
        # releasing camera
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        return ret, frame

    def animate(self, s, q):
        self.xvals = np.append(self.xvals, q)
        self.yvals = np.append(self.yvals, s)

    def get_2d_points(self, img, rotation_vector, translation_vector, camera_matrix, val):
        point_3d = []
        dist_coeffs = np.zeros((4, 1))
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

    def head_pose_points(self, img, rotation_vector, translation_vector, camera_matrix):
        rear_size = 1
        rear_depth = 0
        front_size = img.shape[1]
        front_depth = front_size*2
        val = [rear_size, rear_depth, front_size, front_depth]
        point_2d = self.get_2d_points(img, rotation_vector,
                                      translation_vector, camera_matrix, val)
        y = (point_2d[5] + point_2d[8])//2
        x = point_2d[2]

        return (x, y)

    def check_for_room_light_intensity(self, frame):
        rects = find_faces(frame, self.face_model)
        print(rects)
        if len(rects) == 0:
            return False
        return True

    def calibrate_user_lip_distance(self, frame):
        rects = find_faces(frame, self.face_model)
        self.size = frame.shape
        if len(rects) != 0:
            for rect in rects:
                shapes = detect_marks(frame, self.landmark_model, rect)
            for i in range(100):
                for i, (p1, p2) in enumerate(self.outer_points):
                    self.d_outer[i] += shapes[p2][1] - shapes[p1][1]
                for i, (p1, p2) in enumerate(self.inner_points):
                    self.d_inner[i] += shapes[p2][1] - shapes[p1][1]
            self.after_math()
        return

    def calibrating_user_orientation(self, frame):
        self.orient.append(self.predict(frame))

    def check_calibrated_user_orient(self):
        # after calibrating_user_orientation got run for 15 sec
        self.base = np.mean(self.orient)
        print('base: ', self.base)
        if self.base > 0.9:
            return False  # i.e. user hasn't been calibrated successfully
        return True

    def reset_plot_values(self):
        self.xvals = np.array([])
        self.yvals = np.array([])

    def save_graph(self):
        np.savetxt('xvals.txt', self.xvals, fmt="%f")
        np.savetxt('yvals.txt', self.yvals, fmt='%f')

    def predict(self, frame):
        rects = find_faces(frame, self.face_model)
        nfaces = len(rects)
        # for rect in rects:
        #     cv2.rectangle(frame,(rect[0],rect[1]),(rect[2],rect[3]),(255, 0, 0),3)
        # cv2.imwrite('image'+str(self.i)+'.png',frame)
        # self.i += 1
        if self.TAB_CHANGE == True:
            self.TAB_CHANGE = False
            return 1
        try:
            if nfaces != 0:
                for face in rects:
                    marks = detect_marks(frame, self.landmark_model, face)
                    # mark_detector.draw_marks(img, marks, color=(0, 255, 0))
                    cnt_outer = 0
                    cnt_inner = 0
                    image_points = np.array([marks[30],     # Nose tip
                                            marks[8],     # Chin
                                            # Left eye left corner
                                             marks[36],
                                             # Right eye right corne
                                             marks[45],
                                             marks[48],     # Left Mouth corner
                                             # Right mouth corner
                                             marks[54]
                                             ], dtype="double")

                    # Assuming no lens distortion
                    dist_coeffs = np.zeros((4, 1))

                    (success, rotation_vector, translation_vector) = cv2.solvePnP(
                        self.model_points, image_points, self.camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_UPNP)

                    (nose_end_point2D, jacobian) = cv2.projectPoints(np.array(
                        [(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, self.camera_matrix, dist_coeffs)

                    p1 = (int(image_points[0][0]), int(image_points[0][1]))
                    p2 = (int(nose_end_point2D[0][0][0]),
                          int(nose_end_point2D[0][0][1]))
                    x1, x2 = self.head_pose_points(
                        frame, rotation_vector, translation_vector, self.camera_matrix)

                    classIds, confs, bbox = self.net.detect(
                        frame, confThreshold=self.thres)
                    # print(classIds,confs,bbox)
                    if len(classIds) != 0:
                        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                            if classId == 77:
                                c = confidence
                                # flag=1
                            else:
                                c = 0
                    try:
                        m = (p2[1] - p1[1])/(p2[0] - p1[0])
                        ang1 = int(math.degrees(math.atan(m)))
                        ang1 = ang1/90
                    except:
                        ang1 = 90
                        ang1 = ang1/90

                    try:
                        m = (x2[1] - x1[1])/(x2[0] - x1[0])
                        ang2 = int(math.degrees(math.atan(-1/m)))
                        ang2 = ang2/90
                    except:
                        ang2 = 90/90

                    for i, (m1, m2) in enumerate(self.outer_points):
                        if self.d_outer[i] + 3 < marks[m2][1] - marks[m1][1]:
                            cnt_outer += 1
                    cnt_outer = cnt_outer/5

                    for i, (m1, m2) in enumerate(self.inner_points):
                        if self.d_inner[i] + 2 < marks[m2][1] - marks[m1][1]:
                            cnt_inner += 1
                    cnt_inner = cnt_inner/3

                    # print([nfaces,ang1,ang2,cnt_outer,cnt_inner,c])
                    x = pd.DataFrame(
                        np.array([nfaces, ang1, ang2, cnt_outer, cnt_inner, c]).reshape(1, -1))
                    # print(x)
                #cv2.putText(img, 'Orient', (30, 30), font,1, (0, 255, 255), 2)

                s = final_predictor(x)
                if c == 0:
                    che = s-self.base
                    print(che)
                    self.animate(che, self.q)
                    self.q = self.q+1
                else:
                    che = 1
                    print(che)
                    self.animate(che, self.q)
                    self.q = self.q+1
                if self.STATE == 'TEST_INPROCESS':
                    self.CHEAT = True
                return s
            else:
                return 1  # cheating behaviour
        except Warning:
            return 1  # cheating behaviour

    def after_math(self):
        # after calibrate_user_lip_distannce
        self.d_outer[:] = [x / 100 for x in self.d_outer]
        self.d_inner[:] = [x / 100 for x in self.d_inner]
        self.model_points = np.array([
                                    (0.0, 0.0, 0.0),             # Nose tip
                                    (0.0, -330.0, -65.0),        # Chin
            # Left eye left corner
                                    (-225.0, 170.0, -135.0),
            # Right eye right corne
                                    (225.0, 170.0, -135.0),
            # Left Mouth corner
                                    (-150.0, -150.0, -125.0),
            # Right mouth corner
                                    (150.0, -150.0, -125.0)
        ])
        focal_length = self.size[1]
        center = (self.size[1]/2, self.size[0]/2)
        self.camera_matrix = np.array(
            [[focal_length, 0, center[0]],
             [0, focal_length, center[1]],
             [0, 0, 1]], dtype="double"
        )
