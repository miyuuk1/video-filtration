import numpy as np


class KalmanFilter:
    def __init__(self, shape):
        self.x_asterisk_i = np.zeros(shape)
        self.x_asterisk_prev = np.zeros(shape)
        self.x_hat_i = np.zeros(shape)
        self.P_asterisk_i = np.zeros(shape)
        self.P_asterisk_prev = np.zeros(shape)
        self.P_hat_i = np.zeros(shape)

        self.gamma_i = 1
        self.H_i = np.ones(1)
        self.D_n_i = np.ones(1)
        self.y_i = np.ones(1)
        self.A_i = np.ones(1)
        self.A_prev = np.ones(1)
        self.F_i = np.ones(1)
        self.D_eps_i = np.ones(1)

        # self.xhat = np.zeros(shape)
        # self.xhat_prev = np.zeros(shape)
        # self.P = np.ones(shape)
        # self.P_prev = np.zeros(shape)
        # self.K = np.zeros(shape)
        #
        # self.Q = np.ones(shape) * 1e-10
        # self.R = np.ones(shape) * 1e0
        # self.H = np.ones(shape)
        #
        # self.P = np.ones(shape)

    def update(self, frame):
        self.y_i = frame

        self.x_asterisk_i = self.x_hat_i + self.gamma_i * self.P_asterisk_i * self.H_i.transpose() * (
                    self.D_n_i ** -1) * (self.y_i - self.H_i * self.x_hat_i)
        self.x_hat_i = self.A_prev * self.x_asterisk_prev
        self.P_asterisk_i = self.P_hat_i - self.gamma_i * self.P_hat_i * self.H_i.transpose() * (
                    self.D_n_i + self.H_i * self.P_hat_i * self.H_i.transpose()) ** -1 * self.H_i * self.P_hat_i
        self.P_hat_i = self.A_prev * self.P_asterisk_prev * self.A_prev.transpose() + self.F_i * self.D_eps_i * self.F_i.transpose()

        # self.xhat_prev = self.xhat
        # self.P_prev = self.P + self.Q
        # self.K = self.P_prev * self.H / (self.H * self.P_prev * self.H + self.R)
        # self.xhat = self.xhat_prev + self.K * (frame - self.xhat_prev)
        # self.P = (1 - self.K * self.H) * self.P_prev
        #
        #
        # xhat_prev == x_hat_i
        # P_prev == P_hat_i
        # xhat == x_asterisk_i
        # P == P_asterisk_i
        #
        # Q == D_eps_i
        # H == H_i
        # R ==
        # K == gamma_i * P_asterisk_i*H_i.transpose() * D_n_i**-1
