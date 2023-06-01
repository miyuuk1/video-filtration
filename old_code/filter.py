import numpy as np

class Kalman:
    xhat = 0
    xhat_prev = 0
    P = 0
    P_prev = 0
    K = 0

    Q = 0
    R = 0
    
    def __init__(self):
        pass
    def init(self, r, c):
        self.xhat = np.zeros((r, c))
        self.xhat_prev = np.zeros((r, c))
        self.P = np.ones((r, c))
        self.P_prev = np.zeros((r, c))
        self.K = np.zeros((r, c))

        self.Q = np.ones((r, c)) * 1e-10
        self.R = np.ones((r, c)) * 1e0
        
    def update(self, frame):
        self.xhat_prev = self.xhat
        self.P_prev = self.P + self.Q
        self.K= self.P_prev / (self.P_prev + self.R)
        self.xhat= self.xhat_prev + self.K * (frame - self.xhat_prev)
        self.P = (1 - self.K) * self.P_prev