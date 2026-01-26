"""
Hardware Bridge for Mars-Rover-Control-OS.
HAL for interfacing with motors and sensors.
"""

class HardwareBridge:
    def __init__(self):
        self.connected = False

    def connect(self):
        """
        Establishes connection to the hardware drivers.
        """
        print("Connecting to Rover Hardware Interconnect...")
        self.connected = True

    def write_motor_pwm(self, left_pwm, right_pwm):
        """
        Writes PWM values to the motor controllers.
        """
        if not self.connected: return
        # low-level write logic
        pass

    def read_sensors(self):
        """
        Reads data from all physical sensors.
        """
        if not self.connected: return {}
        # returns dict of sensor readings
        return {"imu": [0,0,0], "encoders": [0,0]}
