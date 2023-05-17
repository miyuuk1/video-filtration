import numpy as np
import cv2


def d_curr_prev(currf_block, prevf_block, N):
    diff = currf_block - prevf_block
    norm2 = np.linalg.norm(diff)
    return norm2 / N ** 2


def motion_compensation(frame, prev_frame):
    BLOCK_SIZE = 4
    bprev_x = 0
    bprev_y = 0
    bcurr_x = 0
    bcurr_y = 0

    xblocks = frame.shape[1] // BLOCK_SIZE
    yblocks = frame.shape[0] // BLOCK_SIZE

    ds = np.zeros((xblocks, yblocks))

    for i in range(xblocks):
        bcurr_x = bprev_x + BLOCK_SIZE
        for j in range(yblocks):
            bcurr_y = bprev_y + BLOCK_SIZE
            current_frame_block = frame[bprev_y:bcurr_y, bprev_x:bcurr_x]
            prev_frame_block = prev_frame[bprev_y:bcurr_y, bprev_x:bcurr_x]

            dcp = d_curr_prev(current_frame_block, prev_frame_block, BLOCK_SIZE)
            ds[i, j] = dcp + 1e-10

            bprev_y = bcurr_y

        bprev_y = 0
        bprev_x = bcurr_x

    # print(ds)
    return ds


def fill_q(q, dm):
    BLOCK_SIZE = 16
    bprev_x = 0
    bprev_y = 0
    bcurr_x = 0
    bcurr_y = 0

    xblocks = q.shape[1] // BLOCK_SIZE
    yblocks = q.shape[0] // BLOCK_SIZE

    for i in range(xblocks):
        bcurr_x = bprev_x + BLOCK_SIZE
        for j in range(yblocks):
            bcurr_y = bprev_y + BLOCK_SIZE

            q[bprev_y:bcurr_y, bprev_x:bcurr_x] = (q[bprev_y:bcurr_y, bprev_x:bcurr_x] * 0) + dm[i][j]

            bprev_y = bcurr_y

        bprev_y = 0
        bprev_x = bcurr_x
    return q


def preprocess_frame(frame, prevs):
    frame = frame.reshape((frame.shape[1], frame.shape[0]))
    blured = cv2.GaussianBlur(frame, (9, 9), 0.9)
    # cv2.imwrite('test/gaussian.jpg', blured)
    last = blured
    dsum = motion_compensation(last, prevs)

    return dsum