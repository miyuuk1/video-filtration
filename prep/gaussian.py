import cv2
import numpy as np
import preprocess_func

# cap = cv2.VideoCapture('..\\test\\output_static_noise.avi')
cap = cv2.VideoCapture('..\\test\\color_test.mp4')

_, frame = cap.read()
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

blured = cv2.GaussianBlur(frame, (11, 11), 3)
cv2.imwrite('frame_611_d5.jpg', blured)

tmp = blured
prev = []
for i in range(0, 10):
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    prev.append(tmp)
    blured = cv2.GaussianBlur(frame, (13, 13), 15)
    cv2.imwrite('frame_11' + str(i) + '_d5.jpg', blured)

    tmp = np.absolute(tmp - blured)

cv2.imwrite('tmp.jpg', tmp)

cap.release()