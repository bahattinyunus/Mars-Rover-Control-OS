"""
Drive Node for Mars-Rover-Control-OS.
Orchestrates motor commands based on high-level navigation goals.
"""

import time
from .pid_controller import PIDController
from .kinematics import RoverKinematics

class DriveNode:
    def __init__(self, config):
        self.kinematics = RoverKinematics(
            wheel_radius=config['wheel_radius'],
            track_width=config['track_width']
        )
        
        self.left_pid = PIDController(kp=config['kp'], ki=config['ki'], kd=config['kd'])
        self.right_pid = PIDController(kp=config['kp'], ki=config['ki'], kd=config['kd'])
        
        self.current_linear_vel = 0.0
        self.current_angular_vel = 0.0
        self.last_update_time = time.time()

    def process_command(self, target_linear_vel, target_angular_vel):
        """
        Processes a velocity command.
        """
        now = time.time()
        dt = now - self.last_update_time
        self.last_update_time = now
        
        # Calculate target wheel velocities
        target_left_rads, target_right_rads = self.kinematics.inverse_kinematics(
            target_linear_vel, target_angular_vel
        )
        
        # Set PID setpoints
        self.left_pid.set_setpoint(target_left_rads)
        self.right_pid.set_setpoint(target_right_rads)
        
        # Note: In a real ROS2 node, we would read actual wheel velocities here
        # For this simulation, we'll assume we're calculating motor PWM/effort
        left_effort = self.left_pid.update(0.0, dt) # Placeholder measurement
        right_effort = self.right_pid.update(0.0, dt) # Placeholder measurement
        
        return left_effort, right_effort

    def update_odometry(self, left_encoder, right_encoder):
        """
        Updates internal state based on encoder feedback.
        """
        self.current_linear_vel, self.current_angular_vel = self.kinematics.forward_kinematics(
            left_encoder, right_encoder
        )
        return self.current_linear_vel, self.current_angular_vel
