import cv2
import numpy as np
import random
from PIL import Image

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('test\\output.avi', fourcc, 30, (960, 600), False)

noises = []
for i in range(30):
    noises.append(random.uniform(0., 100))

# for i in range(3, len(noises)):
#     avg = 0
#     for j in range(3):
#         avg = avg + noises[i-j]
#     noises[i] = avg / 3
        
cnt = 0

frame_count = 1200
im = cv2.imread('samples/halftone.jpg')
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
for i in range(frame_count):

##################################
    # noise
    # print(noises[cnt-1])
    noised = np.zeros((gray.shape[0], gray.shape[1]))
    # noise = np.max(gray) * np.random.normal(0, noises[cnt-1], gray.shape[0] * gray.shape[1]).reshape(gray.shape)
    noise = np.max(gray) * np.random.normal(0, 10, gray.shape[0] * gray.shape[1]).reshape(gray.shape)
    # print(noise.shape)
    noised = gray + noise
############################

    # cv2.imshow('video feed', frame)
    # cv2.imshow('gray feed', noised)
    impath = 'test\\tmp_image.jpg'
    cv2.imwrite(impath, noised)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    loaded = cv2.imread(impath, cv2.IMREAD_GRAYSCALE)
    # cv2.imshow('loaded', im)
    out.write(loaded)


out.release()
cv2.destroyAllWindows()
