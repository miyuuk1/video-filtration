import random
import cv2
import numpy as np
from PIL import Image


def load_image(filename):
    img = Image.open(filename).convert("L")
    img.load()
    h = img.height
    w = img.width
    data = np.asarray(img, dtype="float64")
    return data, h, w


def noiser(nframes, noise_high, noise_low):
    X, h, w = load_image('samples/fields.jpg')
    iters = nframes
    Xs = np.zeros((X.shape[0], X.shape[1], iters))
    for i in range(iters):
        noise = random.uniform(noise_low, noise_high) * np.max(X) * np.random.normal(0, 1, X.shape[0] * X.shape[1]).reshape(
            X.shape)
        Xs[:, :, i] = X + noise

    frame_size = (w, h)
    out = cv2.VideoWriter('output/noised.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, frame_size)
    for i in range(iters):
        out.write(Xs[:, :, i])

    out.release()


def main():
    noiser(10 * 30, 0.99, 0.25)


if __name__ == "__main__":
    main()
