import cv2

from common import common
from kalman import *
from video_func import *
from preprocess_func import *
from optimal.optimal import *


TMP_PATH = 'tmp.jpg'


def init_video(cap_path, out_path):
    cap = open_video(cap_path)
    out, h, w = open_writer(cap, out_path)
    return cap, out, h, w


def process_frame(kf, frame, gamma, out):
    greyscale = frame
    kf.update(greyscale, gamma)

    cv2.imwrite(TMP_PATH, kf.xhat)
    t = cv2.imread(TMP_PATH, cv2.IMREAD_GRAYSCALE)
    out.write(t)


def main_process(input_path, output):
    cap, out, h, w = init_video(input_path, output)
    FRAMES_COUNT = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(FRAMES_COUNT)
    print(cap.get(cv2.CAP_PROP_FPS))

    frames = []
    for i in range(FRAMES_COUNT):
        _, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frames.append(frame)
    cap.release()

    shape = frames[0].shape
    kf = KalmanFilter(shape)

    P_noised = []
    for i in range(FRAMES_COUNT):
        kf.process_p(1)
        P_noised.append(kf.P)

    plan = get_plan(P_noised)
    kf.reset()
    for i in range(len(plan)):
        kf.process_p(plan[i])
        P_noised[i] = kf.P

    plan = get_plan(P_noised)
    file = open(common.DEF_DEBUG_TEXT + "second_plan.txt", "w")
    file.write(str(plan))

    kf.reset()
    kf.xhat = frames[0]
    for i in range(FRAMES_COUNT-1):
        process_frame(kf, frames[i], plan[i], out)

    out.release()
