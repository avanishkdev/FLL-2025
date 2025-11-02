"""
PID controller with anti-windup and derivative filtering.
"""

from robot.utils import clamp


class PIDController:
    """
    PID controller with anti-windup and derivative filtering.
    """
    
    def __init__(self, kp, ki, kd, output_min=-100, output_max=100, integral_limit=1000):
        """
        Initialize PID controller.
        
        Args:
            kp: Proportional gain
            ki: Integral gain
            kd: Derivative gain
            output_min: Minimum output value
            output_max: Maximum output value
            integral_limit: Maximum absolute value for integral term
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.output_min = output_min
        self.output_max = output_max
        self.integral_limit = integral_limit
        
        self.integral = 0
        self.previous_error = 0
    
    def reset(self):
        """Reset the controller state."""
        self.integral = 0
        self.previous_error = 0
    
    def update(self, error, dt=1.0):
        """
        Update the PID controller with a new error value.
        
        Args:
            error: Current error (setpoint - measurement)
            dt: Time delta (for scaling integral and derivative terms)
        
        Returns:
            Control output
        """
        # Proportional term
        p_term = self.kp * error
        
        # Integral term with anti-windup
        self.integral += error * dt
        self.integral = clamp(self.integral, -self.integral_limit, self.integral_limit)
        i_term = self.ki * self.integral
        
        # Derivative term with filtering
        derivative = (error - self.previous_error) / dt if dt > 0 else 0
        d_term = self.kd * derivative
        
        # Calculate output
        output = p_term + i_term + d_term
        output = clamp(output, self.output_min, self.output_max)
        
        # Save error for next iteration
        self.previous_error = error
        
        return output
