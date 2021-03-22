import cv2
import numpy as np

from face_detector import get_face_detector, find_faces


face_model = get_face_detector()
cap = cv2.VideoCapture(0)
while(True):
    ret, img = cap.read()
    rects = find_faces(img, face_model)
    rects = find_faces(img, face_model)
    print(len(rects))
    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
#modelFile =  "models/res10_300x300_ssd_iter_140000.caffemodel"
#configFile = "models/deploy.prototxt"
#net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
#video_capture = cv2.VideoCapture(0)
#while True:
#    
#    ret, frame = video_capture.read()
#    frame = imutils.resize(frame, width=750)
#
#    # grab the frame dimensions and convert it to a blob
#    (h, w) = frame.shape[:2]
#    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
#        (300, 300), (104.0, 177.0, 123.0))
#
#
#    net.setInput(blob)
#    detections = net.forward()
#
#    # loop over the detections
#    for i in range(0, detections.shape[2]):
#        confidence = detections[0, 0, i, 2]
#
#        # filter out weak detections by ensuring the `confidence` is
#        if confidence < 0.5:
#            continue
#
#        # compute the (x, y)-coordinates of the bounding box for the
#        # object
#        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
#        (startX, startY, endX, endY) = box.astype("int")
#
#
#        # draw the bounding box of the face along with the associated
#        # probability
#        text = "{:.2f}%".format(confidence * 100)
#        y = startY - 10 if startY - 10 > 10 else startY + 10
#        cv2.rectangle(frame, (startX, startY), (endX, endY),
#            (0, 0, 255), 2)
#        cv2.putText(frame, text, (startX, y),
#            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
#        print(confidence)
#    # show the output frame
#    cv2.imshow("Frame", frame)
#    key = cv2.waitKey(1) & 0xFF
#
#    # if the `q` key was pressed, break from the loop
#    if key == ord("q"):
#        break
#    
## do a bit of cleanup
#cv2.destroyAllWindows()
#video_capture.release()
