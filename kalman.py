import numpy as np
import cv2

from filter import *

def initVideoOutput(cap):
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter('test\\filter_output.avi', fourcc, fps, (w, h), False)
    return out

def dCurrPrev(currf_block, prevf_block, N):
    diff = currf_block - prevf_block
    norm2 = np.linalg.norm(diff)
    return norm2 / N**2


def MotionCompensation(frame, prev_frame):
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
            
            dcp = dCurrPrev(current_frame_block, prev_frame_block, BLOCK_SIZE)
            ds[i, j] = dcp
            
            bprev_y = bcurr_y
        
        bprev_y = 0
        bprev_x = bcurr_x
    
    # print(ds)
    return ds


def fillQ(q, dm):
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


def main():
    cap = cv2.VideoCapture('test/output.avi')
    out = initVideoOutput(cap)
    kf = Kalman()
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    kf.init(w, h)

    prev_frame = np.zeros((w, h))
    prevs = [prev_frame] * 5
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = frame.reshape((frame.shape[1], frame.shape[0]))
        ## Gaussian Blur
        blured = cv2.GaussianBlur(frame, (9, 9), 0)
        # cv2.imwrite('test/gaussian.jpg', blured)
        last = blured
        dsum = 0    
        for i in range(len(prevs)-1, 0, -1):
            dsum = dsum + MotionCompensation(last, prevs[i])
            last = prevs[i]
        dm = dsum / 5
        
        kf.Q = fillQ(kf.Q, dm)    
    
        kf.update(frame)
        
        prev_frame = kf.xhat
        for i in range(len(prevs)-1):
            prevs[i] = prevs[i+1]
        prevs[len(prevs)-1] = prev_frame
        cv2.imwrite('tmp.jpg', kf.xhat.reshape(h, w))
        t = cv2.imread('tmp.jpg', cv2.IMREAD_GRAYSCALE)
        out.write(t)
        
    cap.release()
    out.release()

if __name__ == "__main__":
    main()
