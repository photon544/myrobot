import cv2
import numpy as np 
cap = cv2.VideoCapture(0)
# ret = cap.set(3, 320)
# ret = cap.set(4, 240)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
i = 0
while cap.isOpened():
    ret, frame = cap.read()
    left_img = frame[:, 0:640, :]
    right_img = frame[:, 640:1280, :]
    if ret:
        #cv2.imshow('img', frame)
        cv2.imshow('left', left_img)
        cv2.imshow('right', right_img)
    key = cv2.waitKey(delay=2)
    if key == ord('t'):
        cv2.imwrite('./img/test' + str(i) + '.jpg', frame)
        i += 1
    if key == ord("q") or key == 27:
        break
cap.release()
cv2.destroyAllWindows()
