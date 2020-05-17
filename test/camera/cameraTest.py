import cv2
cap1 = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
cv2.VideoCapture.set(cap1, 3, 270)
cv2.VideoCapture.set(cap1, 4, 270)
cap2 = cv2.VideoCapture(2 + cv2.CAP_DSHOW)
cv2.VideoCapture.set(cap2, 3, 1)
cv2.VideoCapture.set(cap2, 4, 1)

ret1, frame1 = cap1.read()
ret2, frame2 = cap2.read()

while ret1 and ret2:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    cv2.imshow('frame1', frame1)
    cv2.imshow('frame2', frame2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cap1.release()
cv2.destroyAllWindows()
