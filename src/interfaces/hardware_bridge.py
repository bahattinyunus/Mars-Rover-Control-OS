"""
Hardware Bridge for Mars-Rover-Control-OS.
Industrial-grade HAL with register-level simulation for motor control.
"""

class HardwareBridge:
    # Simulated Device Registers
    REG_MOTOR_L_CONTROL = 0x01
    REG_MOTOR_R_CONTROL = 0x02
    REG_MOTOR_PWM_LIMIT = 0x03
    REG_STATUS_FLAGS    = 0x04

    def __init__(self):
        self.registers = {
            self.REG_MOTOR_L_CONTROL: 0,
            self.REG_MOTOR_R_CONTROL: 0,
            self.REG_MOTOR_PWM_LIMIT: 255,
            self.REG_STATUS_FLAGS: 0
        }
        self._connected = False

    def connect(self):
        """
        Initializes the low-level bus (e.g., CAN or I2C) for communication.
        """
        print("HAL: Initializing high-speed CAN bus...")
        self._connected = True
        self.registers[self.REG_STATUS_FLAGS] |= 0x01 # Set 'Ready' flag

    def write_motor_pwm(self, left_pwm, right_pwm):
        """
        Writes PWM values after safety clipping and register mapping.
        """
        if not self._connected:
            raise ConnectionError("HAL: Peripheral not connected.")

        # Safety Clipping
        limit = self.registers[self.REG_MOTOR_PWM_LIMIT]
        left_pwm = max(-limit, min(limit, left_pwm))
        right_pwm = max(-limit, min(limit, right_pwm))

        # Register Mapping
        self.registers[self.REG_MOTOR_L_CONTROL] = int(left_pwm)
        self.registers[self.REG_MOTOR_R_CONTROL] = int(right_pwm)
        
        print(f"HAL: Dispatched PWM L:{left_pwm} R:{right_pwm} to motor controller.")

    def read_telemetry(self):
        """
        Reads raw register data and translates it to engineering units.
        """
        if not self._connected: return {}
        # Simulate reading encoder counts and IMU data from registers
        return {
            "enc_l": self.registers.get(0x05, 0),
            "enc_r": self.registers.get(0x06, 0),
            "temp": 25.4, # Martian thermal reading
            "status": bin(self.registers[self.REG_STATUS_FLAGS])
        }
        
    def emergency_stop(self):
        """
        Triggers hardware-level emergency stop by zeroing all control registers.
        """
        self.registers[self.REG_MOTOR_L_CONTROL] = 0
        self.registers[self.REG_MOTOR_R_CONTROL] = 0
        self.registers[self.REG_STATUS_FLAGS] |= 0x80 # Set 'ESTOP' flag
        print("HAL: CRITICAL - EMERGENCY STOP TRIGGERED.")
