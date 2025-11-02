"""Motor controller for encoder-based distance control."""

from robot.utils import clamp, sign


class MotorController:
    """Motor controller with encoder-based distance control."""
    
    def __init__(self, motor, positive_direction, ticks_per_rev, max_speed=100, max_deg_per_sec=1080):
        """
        Initialize motor controller.
        
        Args:
            motor: Pybricks Motor object
            positive_direction: Direction multiplier (1 or -1)
            ticks_per_rev: Encoder ticks per revolution (360 for Pybricks)
            max_speed: Maximum speed in numeric scale (-100 to 100)
            max_deg_per_sec: Maximum degrees per second for motor.run()
        """
        self.hw = motor  # Hardware motor object
        self.positive_direction = positive_direction
        self.ticks_per_rev = ticks_per_rev
        self.max_speed = max_speed
        self.max_deg_per_sec = max_deg_per_sec
    
    def _scale_to_deg_per_sec(self, speed):
        """Convert numeric speed (-100 to 100) to deg/s."""
        # Clamp speed to max_speed range
        speed = clamp(speed, -self.max_speed, self.max_speed)
        # Scale to deg/s range
        return (speed / 100.0) * self.max_deg_per_sec
    
    def run(self, speed):
        """
        Run motor at specified speed.
        
        Args:
            speed: Speed in numeric scale (-100 to 100)
        """
        deg_per_sec = self._scale_to_deg_per_sec(speed * self.positive_direction)
        self.hw.run(deg_per_sec)
    
    def stop(self):
        """Stop the motor."""
        self.hw.stop()
    
    def reset_angle(self, angle=0):
        """Reset encoder angle."""
        self.hw.reset_angle(angle)
    
    def angle(self):
        """Get current encoder angle in degrees."""
        return self.hw.angle() * self.positive_direction
    
    def drive_to_distance(self, distance_ticks, speed, kp=1.0):
        """
        Drive motor to a target distance using encoder feedback.
        
        Args:
            distance_ticks: Target distance in encoder ticks
            speed: Maximum speed in numeric scale
            kp: Proportional gain for distance control
        
        Returns:
            True when target reached
        """
        current_angle = self.angle()
        error = distance_ticks - current_angle
        
        # Calculate speed based on error
        control_speed = kp * error
        control_speed = clamp(control_speed, -abs(speed), abs(speed))
        
        # Check if reached target
        if abs(error) < 5:  # Small tolerance
            self.stop()
            return True
        
        self.run(control_speed)
        return False
