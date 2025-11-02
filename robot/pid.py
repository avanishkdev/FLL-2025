"""PID controller with anti-windup and derivative filtering."""

from robot.utils import clamp


class PID:
    """PID controller with anti-windup and optional derivative filtering."""
    
    def __init__(self, kp, ki, kd, integral_limit=None, derivative_filter=0.0):
        """
        Initialize PID controller.
        
        Args:
            kp: Proportional gain
            ki: Integral gain
            kd: Derivative gain
            integral_limit: Maximum absolute value for integral term (None for no limit)
            derivative_filter: Filter coefficient for derivative (0.0 = no filter, higher = more filtering)
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral_limit = integral_limit
        self.derivative_filter = derivative_filter
        
        self.integral = 0
        self.prev_error = 0
        self.filtered_derivative = 0
    
    def reset(self):
        """Reset PID state."""
        self.integral = 0
        self.prev_error = 0
        self.filtered_derivative = 0
    
    def compute(self, error, dt=1.0):
        """
        Compute PID output.
        
        Args:
            error: Current error value
            dt: Time step (default 1.0)
        
        Returns:
            PID output value
        """
        # Proportional term
        p_term = self.kp * error
        
        # Integral term with anti-windup
        self.integral += error * dt
        if self.integral_limit is not None:
            self.integral = clamp(self.integral, -self.integral_limit, self.integral_limit)
        i_term = self.ki * self.integral
        
        # Derivative term with optional filtering
        raw_derivative = (error - self.prev_error) / dt if dt > 0 else 0
        if self.derivative_filter > 0:
            self.filtered_derivative = (
                self.derivative_filter * self.filtered_derivative +
                (1 - self.derivative_filter) * raw_derivative
            )
            derivative = self.filtered_derivative
        else:
            derivative = raw_derivative
        d_term = self.kd * derivative
        
        self.prev_error = error
        
        return p_term + i_term + d_term
