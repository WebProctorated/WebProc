import numpy as np
import cv2

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
count = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame,1)

        out.write(frame)

        img = cv2.imshow('frame',frame)
        cv2.imwrite('images.jpg',img)
        
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lowskin = np.array([108, 23, 82])
        highskin = np.array([179, 255, 255])
        mask = cv2.inRange(hsv_frame, lowskin, highskin)
        cv2.imshow("mask", mask)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif cv2.waitKey(1) & 0xFF == ord('a') :
            print("image"+str(count)+'saved')
            file = 'D:/image+video/img'+str(count)+'.png'
            cv2.imwrite(file,img)
            count += 1
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
