"""
Basic Unit Tests for Mars-Rover-Control-OS.
Tests PID controller and Kinematics.
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from control.pid_controller import PIDController
from control.kinematics import RoverKinematics

class TestControlSystems(unittest.TestCase):
    def test_pid_logic(self):
        pid = PIDController(kp=1.0, ki=0.0, kd=0.0, setpoint=10.0)
        output = pid.update(measurement=5.0, dt=1.0)
        self.assertEqual(output, 5.0)

    def test_kinematics_inverse(self):
        kin = RoverKinematics(wheel_radius=0.1, track_width=0.5)
        # linear= velocity=1.0, angular=0.0 -> both wheels should be 10.0 rad/s
        left, right = kin.inverse_kinematics(1.0, 0.0)
        self.assertAlmostEqual(left, 10.0)
        self.assertAlmostEqual(right, 10.0)

if __name__ == '__main__':
    unittest.main()
