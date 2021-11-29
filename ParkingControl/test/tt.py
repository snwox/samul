import cv2

cap=cv2.VideoCapture(0)

if not cap.isOpened():
    print("asdfadsf")
    exit()

while True:
    ret,frame=cap.read()
    if not ret:
        break

    cv2.imshow("frame",frame)
    if cv2.waitKey(10)==27:
        cv2.imwrite('output.jpg',frame)
        break

cap.release()
cv2.destoryAllWindows()