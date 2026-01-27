"""
Sensor Fusion module for Mars-Rover-Control-OS.
Implements a functional Extended Kalman Filter (EKF) to fuse IMU and Odometry.
"""

import numpy as np

class SensorFusion:
    def __init__(self):
        # State vector [x, y, theta, v, omega]
        self.state = np.zeros(5)
        # Covariance matrix
        self.P = np.eye(5) * 0.1
        # Process noise covariance
        self.Q = np.eye(5) * 0.01
        # Measurement noise covariance (Odom)
        self.R_odom = np.diag([0.05, 0.05])
        # Measurement noise covariance (IMU)
        self.R_imu = np.diag([0.01])

    def predict(self, dt):
        """
        Prediction step based on non-linear motion model.
        """
        x, y, theta, v, omega = self.state

        # State transition function f(x, u)
        new_x = x + v * np.cos(theta) * dt
        new_y = y + v * np.sin(theta) * dt
        new_theta = theta + omega * dt
        
        # Predicted state
        self.state = np.array([new_x, new_y, new_theta, v, omega])

        # Jacobian of f (F)
        F = np.eye(5)
        F[0, 2] = -v * np.sin(theta) * dt
        F[0, 3] = np.cos(theta) * dt
        F[1, 2] = v * np.cos(theta) * dt
        F[1, 3] = np.sin(theta) * dt
        F[2, 4] = dt

        # Covariance prediction
        self.P = F @ self.P @ F.T + self.Q

    def update_odom(self, v_measured, omega_measured):
        """
        Update step using wheel odometry measurements.
        """
        z = np.array([v_measured, omega_measured])
        H = np.zeros((2, 5))
        H[0, 3] = 1 # Linear velocity sensor
        H[1, 4] = 1 # Angular velocity sensor

        y = z - (H @ self.state) # Innovation
        S = H @ self.P @ H.T + self.R_odom
        K = self.P @ H.T @ np.linalg.inv(S) # Kalman Gain

        self.state = self.state + (K @ y)
        self.P = (np.eye(5) - (K @ H)) @ self.P

    def update_imu(self, yaw_rate_measured):
        """
        Update step using IMU gyro data (yaw rate).
        """
        z = np.array([yaw_rate_measured])
        H = np.zeros((1, 5))
        H[0, 4] = 1

        y = z - (H @ self.state)
        S = H @ self.P @ H.T + self.R_imu
        K = self.P @ H.T @ np.linalg.inv(S)

        self.state = self.state + (K @ y)
        self.P = (np.eye(5) - (K @ H)) @ self.P

    def get_estimate(self):
        return {
            "pose": self.state[:3],
            "velocity": self.state[3:]
        }
