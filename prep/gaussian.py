import cv2
import numpy as np

cap = cv2.VideoCapture('..\\test\\output_static_noise.avi')

_, frame = cap.read()
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

blured = cv2.GaussianBlur(frame, (11, 11), 3)
cv2.imwrite('frame_611_d5.jpg', blured)

tmp = blured

for i in range(0, 10):
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blured = cv2.GaussianBlur(frame, (11, 11), 3)
    cv2.imwrite('frame_11' + str(i) + '_d5.jpg', blured)

    tmp = np.absolute(tmp - blured) / 2

cv2.imwrite('tmp.jpg', tmp)

cap.release()