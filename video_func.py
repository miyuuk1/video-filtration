import cv2


def open_video(path):
    cap = cv2.VideoCapture(path)
    return cap


def open_writer(cap, out_path):
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    out = cv2.VideoWriter(out_path, fourcc, cap.get(cv2.CAP_PROP_FPS), (int(w), int(h)), False)
    return out, h, w


def close_cap_out(cap, out):
    cap.release()
    out.release()

