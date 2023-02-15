import cv2
import numpy as np
import random
from PIL import Image

cap = cv2.VideoCapture('test\\cut.mp4')
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('test\\output.avi', fourcc, cap.get(cv2.CAP_PROP_FPS), (1280, 720), False)

noises = []
for i in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
    noises.append(random.uniform(0., 1))

for i in range(3, len(noises)):
    avg = 0
    for j in range(3):
        avg = avg + noises[i-j]
    noises[i] = avg / 3
        
cnt = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cnt = cnt + 1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

##################################
    # noise
    # print(noises[cnt-1])
    noised = np.zeros((gray.shape[0], gray.shape[1]))
    noise = np.max(gray) * np.random.normal(0, 1, gray.shape[0] * gray.shape[1]).reshape(gray.shape)
    # noise = np.max(gray) * np.random.normal(0, noises[cnt-1], gray.shape[0] * gray.shape[1]).reshape(gray.shape)
    # print(noise.shape)
    noised = gray + noise
############################

    # cv2.imshow('video feed', frame)
    # cv2.imshow('gray feed', noised)
    impath = 'test\\tmp_image.jpg'
    cv2.imwrite(impath, noised)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    im = cv2.imread(impath, cv2.IMREAD_GRAYSCALE)
    # cv2.imshow('loaded', im)
    out.write(im)


cap.release()
out.release()
cv2.destroyAllWindows()
