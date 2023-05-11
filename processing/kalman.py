import numpy as np


class KalmanFilter:
    def __init__(self, shape):
        self.xhat = np.zeros(shape)
        self.xhat_prev = np.zeros(shape)
        self.P = np.ones(shape)
        self.P_prev = np.zeros(shape)
        self.K = np.zeros(shape)

        self.Q = np.ones(shape) * 1e-10
        self.R = np.ones(shape) * 1e0
        self.H = np.ones(shape)

        self.P = np.ones(shape)

    def update(self, frame):
        self.xhat_prev = self.xhat
        self.P_prev = self.P + self.Q
        self.K = self.P_prev * self.H / (self.H * self.P_prev * self.H + self.R)
        self.xhat = self.xhat_prev + self.K * (frame - self.xhat_prev)
        self.P = (1 - self.K * self.H) * self.P_prev

