"""PID controller with anti-windup and derivative filtering."""

from robot.utils import clamp


class PID:
    """PID controller with anti-windup and derivative filtering."""
    
    def __init__(self, kp, ki, kd, output_limit=100, integral_limit=None):
        """
        Initialize PID controller.
        
        Args:
            kp: Proportional gain
            ki: Integral gain
            kd: Derivative gain
            output_limit: Maximum absolute output value
            integral_limit: Maximum absolute integral value (None for unlimited)
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.output_limit = output_limit
        self.integral_limit = integral_limit if integral_limit is not None else output_limit
        
        self.integral = 0
        self.prev_error = 0
        self.prev_derivative = 0
        
    def reset(self):
        """Reset internal state."""
        self.integral = 0
        self.prev_error = 0
        self.prev_derivative = 0
    
    def update(self, error, dt=1):
        """
        Update PID controller with new error.
        
        Args:
            error: Current error value
            dt: Time delta (for integral/derivative calculation)
            
        Returns:
            Control output
        """
        # Proportional term
        p_term = self.kp * error
        
        # Integral term with anti-windup
        self.integral += error * dt
        self.integral = clamp(self.integral, -self.integral_limit, self.integral_limit)
        i_term = self.ki * self.integral
        
        # Derivative term with filtering (simple low-pass)
        derivative = (error - self.prev_error) / dt
        filtered_derivative = 0.7 * derivative + 0.3 * self.prev_derivative
        d_term = self.kd * filtered_derivative
        
        self.prev_error = error
        self.prev_derivative = filtered_derivative
        
        # Calculate output and clamp
        output = p_term + i_term + d_term
        output = clamp(output, -self.output_limit, self.output_limit)
        
        return output
