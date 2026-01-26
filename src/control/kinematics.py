"""
Kinematics module for Mars-Rover-Control-OS.
Handles differential drive kinematics for a 6-wheel rover system.
"""

import math

class RoverKinematics:
    def __init__(self, wheel_radius, track_width):
        self.wheel_radius = wheel_radius
        self.track_width = track_width

    def inverse_kinematics(self, linear_velocity, angular_velocity):
        """
        Calculate wheel velocities from robot velocity.
        :param linear_velocity: Linear velocity (m/s)
        :param angular_velocity: Angular velocity (rad/s)
        :return: (left_velocity, right_velocity) in rad/s
        """
        left_vel = (linear_velocity - (angular_velocity * self.track_width / 2.0)) / self.wheel_radius
        right_vel = (linear_velocity + (angular_velocity * self.track_width / 2.0)) / self.wheel_radius
        return left_vel, right_vel

    def forward_kinematics(self, left_wheel_vel, right_wheel_vel):
        """
        Calculate robot velocity from wheel velocities.
        :param left_wheel_vel: Left wheel velocity (rad/s)
        :param right_wheel_vel: Right wheel velocity (rad/s)
        :return: (linear_velocity, angular_velocity)
        """
        linear_velocity = (left_wheel_vel + right_wheel_vel) * self.wheel_radius / 2.0
        angular_velocity = (right_wheel_vel - left_wheel_vel) * self.wheel_radius / self.track_width
        return linear_velocity, angular_velocity
