from kalman import *
from video_func import *
import cv2
from sys import argv


def init_video(cap_path, out_path):
    cap = open_video(cap_path)
    out, h, w = open_writer(cap, out_path)
    return cap, out, h, w


def process_frame(kf, frame):
    greyscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    kf.update(greyscale)


# INPUT_PATH = "input.mp4"
# OUTPUT_PATH = "output.mp4"
TMP_PATH = 'tmp.jpg'


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

    for i in range(1, FRAMES_COUNT):
        _, frame = cap.read()
        process_frame(kf, frame)

        cv2.imwrite(TMP_PATH, kf.xhat)

        t = cv2.imread(TMP_PATH, cv2.IMREAD_GRAYSCALE)
        out.write(t)

    close_cap_out(cap, out)


def main():
    if len(argv) < 2:
        print("error: params length < 2: ", argv)
        print("usage: ", argv[0], " <input> <output>")
        return
    input_path = argv[1]
    output = argv[2]

    main_process(input_path, output)


if __name__ == "__main__":
    main()