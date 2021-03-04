import cv2

configPath = './proctoring/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = './proctoring/frozen_inference_graph.pb'
try:
    net = cv2.dnn_DetectionModel(weightsPath,configPath)
except Exception as esp:
    print(esp)

net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def phone_detection(frame):
    print('phone_detection: {}'.format(frame.shape))
    classIds, confs, bbox = net.detect(frame,confThreshold=0.45)
    # print(classIds,confs,bbox)

    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            print('classId: {}, confidence: {}'.format(classId,confidence))
            # if classId == 77 and confidence >= 0:
            if classId == 77:
                print("Yes")
                return True

    return False
