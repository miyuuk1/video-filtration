import random

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2


def load_image(filename):
    img = Image.open(filename).convert("L")
    img.load()
    data = np.asarray(img, dtype="float64")
    return data


def main():
    frame_one, frame_two, frame_three, frame_four = 0, 63, 127, 255

    cap = cv2.VideoCapture('test/output.avi')
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    print(w, h)
    out = cv2.VideoWriter('test\\filter_output.avi', fourcc, cap.get(cv2.CAP_PROP_FPS), (int(w), int(h)), False)
    # X = load_image('samples/fields.jpg')
    # plt.figure(figsize=(10, 10))
    # plt.imshow(X, cmap='gray')

    iters = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    noise_ratio = .99
    ret, frame = cap.read()
    # Xs = np.zeros((h, w, iters))
    # for i in range(iters):
    #     noise = random.uniform(0.25, 0.99) * np.max(frame) * np.random.normal(0, 1, frame.shape[0] * frame.shape[1]).reshape(frame.shape)
    #     Xs[:, :, i] = X + noise
    # plt.figure(figsize=(10, 10))
    # plt.imshow(Xs[:, :, 0], cmap='gray')

    # initialize arrays
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    xhat = np.zeros(frame.shape)
    xhat_prev = np.zeros(frame.shape)
    P = np.ones(frame.shape)
    P_prev = np.zeros(frame.shape)
    K = np.zeros(frame.shape)

    Q = np.ones(frame.shape) * 1e-10
    R = np.ones(frame.shape) * 1e0
    H = np.ones(frame.shape)

    
    xhat = frame
    P = np.ones(frame.shape)

    # apply kalman filter
    for k in range(1, iters):
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        xhat_prev = xhat
        P_prev = P + Q
        K= P_prev * H / (H * P_prev * H + R)
        xhat= xhat_prev + K * (frame - xhat_prev)
        P = (1 - K * H) * P_prev
        cv2.imwrite('tmp.jpg', xhat)
        t = cv2.imread('tmp.jpg', cv2.IMREAD_GRAYSCALE)
        out.write(t)

    cap.release()
    out.release()
    # plt.subplots(nrows=2, ncols=2, figsize=(15, 10))
    # plt.subplot(2, 2, 1)
    # plt.imshow(xhat[:, :, frame_one], cmap='gray')
    # plt.title('Original + Noise')
    # plt.subplot(2, 2, 2)
    # plt.imshow(xhat[:, :, frame_two], cmap='gray')
    # plt.title('iteration = ' + str(frame_two))
    # plt.subplot(2, 2, 3)
    # plt.imshow(xhat[:, :, frame_three], cmap='gray')
    # plt.title('iteration = ' + str(frame_three))
    # plt.subplot(2, 2, 4)
    # plt.imshow(xhat[:, :, frame_four], cmap='gray')
    # plt.title('iteration = ' + str(frame_four))
    # plt.show()

    # plt.figure(figsize=(10, 10))
    # plt.imshow(xhat[:, :, frame_one], cmap='gray')
    # plt.imsave('samples/noisy.jpeg', xhat[:, :, frame_one], cmap='gray')
    # plt.figure(figsize=(10, 10))
    # plt.imshow(xhat[:, :, frame_two], cmap='gray')
    # plt.imsave('samples/iter63.jpg', xhat[:, :, frame_two], cmap='gray')
    # plt.figure(figsize=(10, 10))
    # plt.imshow(xhat[:, :, frame_three], cmap='gray')
    # plt.imsave('samples/iter127.jpg', xhat[:, :, frame_three], cmap='gray')
    # plt.figure(figsize=(10, 10))
    # plt.imshow(xhat[:, :, frame_four], cmap='gray')
    # plt.imsave('samples/iter255.jpg', xhat[:, :, frame_four], cmap='gray')
    # plt.show()


if __name__ == "__main__":
    main()
