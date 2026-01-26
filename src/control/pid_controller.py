"""
PID Controller module for Mars-Rover-Control-OS.
Handles velocity and heading control.
"""

class PIDController:
    def __init__(self, kp, ki, kd, setpoint=0.0, output_limits=(None, None)):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self._output_limits = output_limits
        
        self._prev_error = 0.0
        self._integral = 0.0
        self._last_time = None

    def update(self, measurement, dt):
        """
        Update the PID controller.
        :param measurement: Current measured value
        :param dt: Time since last update
        :return: Control output
        """
        error = self.setpoint - measurement
        
        # Proportional term
        p_term = self.kp * error
        
        # Integral term
        self._integral += error * dt
        i_term = self.ki * self._integral
        
        # Derivative term
        derivative = (error - self._prev_error) / dt if dt > 0 else 0.0
        d_term = self.kd * derivative
        
        output = p_term + i_term + d_term
        
        # Apply output limits
        lower, upper = self._output_limits
        if lower is not None:
            output = max(lower, output)
        if upper is not None:
            output = min(upper, output)
            
        self._prev_error = error
        return output

    def set_setpoint(self, setpoint):
        self.setpoint = setpoint

    def reset(self):
        self._prev_error = 0.0
        self._integral = 0.0
