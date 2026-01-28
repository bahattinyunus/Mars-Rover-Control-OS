"""
Fusion Tests for Mars-Rover-Control-OS.
Validates EKF convergence and state estimation.
"""

import unittest
import sys
import os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from perception.sensor_fusion import SensorFusion

class TestSensorFusion(unittest.TestCase):
    def test_ekf_prediction(self):
        fusion = SensorFusion()
        # Set initial velocity
        fusion.state[3] = 1.0 # 1 m/s
        
        fusion.predict(dt=1.0)
        # after 1s at 1m/s, x should be 1.0
        self.assertAlmostEqual(fusion.state[0], 1.0)

    def test_odom_update(self):
        fusion = SensorFusion()
        # Initial state is 0. Update with velocity measurement
        fusion.update_odom(v_measured=0.5, omega_measured=0.0)
        
        # State velocity should move towards 0.5
        self.assertGreater(fusion.state[3], 0.0)
        self.assertLessEqual(fusion.state[3], 0.5)

    def test_imu_update(self):
        fusion = SensorFusion()
        fusion.update_imu(yaw_rate_measured=0.1)
        # Angular velocity should move towards 0.1
        self.assertGreater(fusion.state[4], 0.0)

if __name__ == '__main__':
    unittest.main()
