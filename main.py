import os
import random
import filterpy.kalman
import filterpy.common
import numpy as np

from PIL import Image
from PIL import ImageDraw
from os import path

DEF_SAMPLES_DIR = "samples"
DEF_OUTPUT_DIR = "output"
DEF_SAMPLE_NAME = "sample.jpg"
DEF_SAMPLE_PATH = path.join(DEF_SAMPLES_DIR, DEF_SAMPLE_NAME)

sig = 0.5
disp = sig * sig


def add_noise(im, sigma):
    mu = 1
    draw = ImageDraw.Draw(im)
    width = im.size[0]
    height = im.size[1]
    pix = im.load()
    for i in range(width):
        for j in range(height):
            rand = random.gauss(mu, sigma)
            # r = pix[i, j][0] + rand
            # g = pix[i, j][1] + rand
            # b = pix[i, j][2] + rand
            # if r < 0: r = 0
            # if g < 0: g = 0
            # if b < 0: b = 0
            # if r > 255: r = 255
            # if g > 255: g = 255
            # if b > 255: b = 255
            c = pix[i, j] + rand
            # draw.point((i, j), (int(r), int(g), int(b)))
            draw.point((i, j), int(c))
    del draw
    return im


def filter_1d(im):
    SKO = sig
    (w, h) = im.size
    draw = ImageDraw.Draw(im)
    pix = im.load()
    kf = filterpy.kalman.KalmanFilter(dim_x=1, dim_z=1)
    kf.F = np.array([[1]])
    kf.H = np.array([[1]])
    # kf.Q = filterpy.common.Q_discrete_white_noise(dim=2, dt=0.1, var=0.1)
    kf.Q = np.array([[1e-10]])
    kf.R = np.array([[1e-4]])
    kf.x = np.array([pix[0, 0]])
    kf.P = np.array([[1000]])
    for i in range(w):
        for j in range(h):
            z = [pix[i, j]]
            kf.predict()
            kf.update(z)
            c = kf.x
            draw.point((i, j), int(c))
    return im


def main():
    im = Image.open(DEF_SAMPLE_PATH).convert("L")
    im.save(path.join(DEF_OUTPUT_DIR, "pure.jpeg"))
    if not path.exists(DEF_OUTPUT_DIR):
        os.mkdir(DEF_OUTPUT_DIR)
    im = add_noise(im, 0.1)
    out = path.join(DEF_OUTPUT_DIR, "noise3.jpeg")
    im.save(out)
    im = Image.open(out)


    out = path.join(DEF_OUTPUT_DIR, "filter3.jpeg")
    im.save(out)


if __name__ == '__main__':
    main()
