import os

import cv2
import numpy as np
import random
import common.common as commons


DEF_CUTSET1_INPUT = commons.DEFAULT_INPUT + "cutset1.mp4"
DEF_CUTSET2_INPUT = commons.DEFAULT_INPUT + "cutset2.mp4"
DEF_CUTSET3_INPUT = commons.DEFAULT_INPUT + "cutset3.mp4"
DEF_CUTSET1_OUTPUT = commons.DEFAULT_OUTPUT + "noised_cutset1.avi"
DEF_CUTSET2_OUTPUT = commons.DEFAULT_OUTPUT + "noised_cutset2.avi"
DEF_CUTSET3_OUTPUT = commons.DEFAULT_OUTPUT + "noised_cutset3.avi"

DEF_DEBUG_CLEAR = commons.DEFAULT_OUTPUT + "cleared\\"
DEF_DEBUG_NOISE = commons.DEFAULT_OUTPUT + "noised\\"
DEF_DEBUG_TEXT = commons.DEFAULT_OUTPUT + "text\\"


def smoother(array, n):
    for i in range(3, len(array)):
        avg = 0
        for j in range(3):
            avg = avg + array[i - j]
        array[i] = avg / 3
    return array


def make_noise(in_path, out_path, disp, debug = False, debug_name = ""):
    cap = cv2.VideoCapture(in_path)
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter(out_path, fourcc, cap.get(cv2.CAP_PROP_FPS), (720, 480), False)

    noises = []
    for i in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
        noises.append(np.random.normal(0., disp, (480, 720)))

    if debug:
        file = open(DEF_DEBUG_TEXT + debug_name + "_noises.txt", "w")
        file.write(str(noises))

    # frames = []
    for i in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if debug:
            cv2.imwrite(DEF_DEBUG_CLEAR + debug_name + "_frame_" + str(i) + ".jpg", gray)

        noised = gray + noises[i]
        if debug:
            cv2.imwrite(DEF_DEBUG_NOISE + debug_name + "_frame_" + str(i) + ".jpg", noised)
            if i < 10:
                np.savetxt(DEF_DEBUG_TEXT + debug_name + "_frame_" + str(i) + ".txt", noised, fmt='%.5f', delimiter='\n')

        impath = '..\\test\\tmp_image.jpg'
        cv2.imwrite(impath, noised)
        im = cv2.imread(impath, cv2.IMREAD_GRAYSCALE)
        out.write(im)

    cap.release()
    out.release()


def main():
    make_noise(DEF_CUTSET1_INPUT, DEF_CUTSET1_OUTPUT, 10, True, "CUTSET1_DISP10")
    make_noise(DEF_CUTSET2_INPUT, DEF_CUTSET2_OUTPUT, 20, True, "CUTSET2_DISP20")
    make_noise(DEF_CUTSET3_INPUT, DEF_CUTSET3_OUTPUT, 30, True, "CUTSET3_DISP30")


if __name__ == "__main__":
    main()