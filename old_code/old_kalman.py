import numpy as np
import cv2


def main():
    # cap = cv2.VideoCapture('test/output.avi')
    # fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    # h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # print(w, h)
    # out = cv2.VideoWriter('test\\filter_output.avi', fourcc, cap.get(cv2.CAP_PROP_FPS)*2, (int(w), int(h)), False)

    # iters = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # ret, frame = cap.read()

    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # xhat = np.zeros(frame.shape)
    # xhat_prev = np.zeros(frame.shape)
    # P = np.ones(frame.shape)
    # P_prev = np.zeros(frame.shape)
    # K = np.zeros(frame.shape)
    #
    # Q = np.ones(frame.shape) * 1e-10
    # R = np.ones(frame.shape) * 1e0
    # H = np.ones(frame.shape)

    
    # xhat = frame
    # P = np.ones(frame.shape)

    # for _ in range(1, iters):
    #     ret, frame = cap.read()
    #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #
    #     xhat_prev = xhat
    #     P_prev = P + Q
    #     K= P_prev * H / (H * P_prev * H + R)
    #     xhat= xhat_prev + K * (frame - xhat_prev)
    #     P = (1 - K * H) * P_prev
    #
    #     cv2.imwrite('tmp.jpg', xhat)
    #     t = cv2.imread('tmp.jpg', cv2.IMREAD_GRAYSCALE)
    #     out.write(t)
    #
    # cap.release()
    # out.release()
    pass

if __name__ == "__main__":
    main()
