import numpy as np
import cv2


def d_curr_prev(currf_block, prevf_block, N):
    dif = prevf_block[0] - currf_block
    for i in range(1, prevf_block):
        dif = np.absolute(prevf_block[i] - dif)
    return  dif / len(prevf_block)




def motion_compensation(frame, prev_frame):
    BLOCK_SIZE = 16
    bprev_x = 0
    bprev_y = 0
    bcurr_x = 0
    bcurr_y = 0

    xblocks = frame.shape[1] // BLOCK_SIZE
    yblocks = frame.shape[0] // BLOCK_SIZE

    prev_n = len(prev_frame)
    dss = [prev_n]
    prev_blocks = [prev_n]
    for f in range(prev_frame):
        ds = np.zeros((xblocks, yblocks))
        bprev_x = 0
        bprev_y = 0
        for i in range(xblocks):
            bcurr_x = bprev_x + BLOCK_SIZE
            for j in range(yblocks):
                bcurr_y = bprev_y + BLOCK_SIZE
                current_frame_block = frame[bprev_y:bcurr_y, bprev_x:bcurr_x]
                for pf in range(prev_frame):
                    prev_blocks[pf] = prev_frame[pf][bprev_y:bcurr_y, bprev_x:bcurr_x]
                # prev_frame_block = prev_frame[bprev_y:bcurr_y, bprev_x:bcurr_x]

                dcp = d_curr_prev(current_frame_block, prev_blocks, BLOCK_SIZE)
                ds[i, j] = dcp + 1e-10

                bprev_y = bcurr_y

            bprev_y = 0
            bprev_x = bcurr_x

        dss[f] = ds

    # print(ds)
    return dss


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

    last = blured
    dsum = motion_compensation(last, prevs)

    return dsum