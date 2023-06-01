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

        self.P = np.ones(shape) * 10

    def update(self, frame, gamma):
        self.xhat_prev = self.xhat
        self.P_prev = self.P + self.Q
        self.K = self.P_prev * self.H / (self.H * self.P_prev * self.H + self.R)
        self.xhat = self.xhat_prev + gamma *  self.K * (frame - self.xhat_prev)
        self.P = (1 - self.K * self.H) * self.P_prev * gamma

    def process_p(self, gamma):
        self.P_prev = self.P + self.Q
        self.K = self.P_prev * self.H / (self.H * self.P_prev * self.H + self.R)
        self.P = (1 - self.K * self.H) * self.P_prev * gamma


    def reset(self):
        self.P = np.ones(self.xhat.shape)
        self.P_prev = np.zeros(self.xhat.shape)
        self.K = np.zeros(self.xhat.shape)

