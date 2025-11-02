"""PID controller with anti-windup and derivative filtering."""

from robot.utils import clamp


class PID:
    """PID controller with anti-windup and derivative filtering."""
    
    def __init__(self, kp, ki, kd, output_min=-100, output_max=100, 
                 integral_max=None, derivative_filter=0.1):
        """
        Initialize PID controller.
        
        Args:
            kp: Proportional gain
            ki: Integral gain
            kd: Derivative gain
            output_min: Minimum output value
            output_max: Maximum output value
            integral_max: Maximum integral term (None = use output_max)
            derivative_filter: Low-pass filter coefficient for derivative (0-1)
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.output_min = output_min
        self.output_max = output_max
        self.integral_max = integral_max if integral_max is not None else output_max
        self.derivative_filter = derivative_filter
        
        self.integral = 0
        self.last_error = None
        self.last_derivative = 0
    
    def reset(self):
        """Reset the PID controller state."""
        self.integral = 0
        self.last_error = None
        self.last_derivative = 0
    
    def update(self, error, dt=0.02):
        """
        Update PID controller with new error value.
        
        Args:
            error: Current error value (setpoint - measured)
            dt: Time delta in seconds (default 0.02 = 50Hz)
        
        Returns:
            Control output value
        """
        # Proportional term
        p_term = self.kp * error
        
        # Integral term with anti-windup
        self.integral += error * dt
        self.integral = clamp(self.integral, -self.integral_max, self.integral_max)
        i_term = self.ki * self.integral
        
        # Derivative term with filtering
        if self.last_error is not None:
            raw_derivative = (error - self.last_error) / dt
            # Apply low-pass filter to reduce noise
            self.last_derivative = (self.derivative_filter * raw_derivative + 
                                   (1 - self.derivative_filter) * self.last_derivative)
            d_term = self.kd * self.last_derivative
        else:
            d_term = 0
        
        self.last_error = error
        
        # Calculate output
        output = p_term + i_term + d_term
        return clamp(output, self.output_min, self.output_max)
