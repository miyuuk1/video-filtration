import cv2
from kalman import *
from video_func import *
from preprocess_func import *


TMP_PATH = 'tmp.jpg'


def init_video(cap_path, out_path):
    cap = open_video(cap_path)
    out, h, w = open_writer(cap, out_path)
    return cap, out, h, w


def process_frame(kf, frame, out, prevs):
    greyscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # dm = preprocess_frame(greyscale, prevs)

    # kf.Q = fill_q(kf.Q, dm)
    kf.update(greyscale)

    cv2.imwrite(TMP_PATH, kf.xhat)

    t = cv2.imread(TMP_PATH, cv2.IMREAD_GRAYSCALE)
    out.write(t)


def main_process(input_path, output):
    cap, out, h, w = init_video(input_path, output)
    FRAMES_COUNT = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(FRAMES_COUNT)
    print(cap.get(cv2.CAP_PROP_FPS))
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    shape = frame.shape
    kf = KalmanFilter(shape)

    kf.xhat = frame

    prev_frame = np.zeros((w, h))
    prevs = prev_frame
    for i in range(1, FRAMES_COUNT):
        _, frame = cap.read()
        process_frame(kf, frame, out, prevs)

    close_cap_out(cap, out)
