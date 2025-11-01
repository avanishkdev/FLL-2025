"""Motor control abstractions with encoder-based movement."""

from robot.utils import sign


class MotorHardware:
    """Abstract interface for motor hardware."""
    
    def get_angle(self):
        """Get current motor angle in degrees."""
        raise NotImplementedError
    
    def reset_angle(self, angle=0):
        """Reset motor angle to specified value."""
        raise NotImplementedError
    
    def run(self, speed):
        """Run motor at specified speed (deg/s)."""
        raise NotImplementedError
    
    def stop(self):
        """Stop the motor."""
        raise NotImplementedError
    
    def hold(self):
        """Hold the motor at current position."""
        raise NotImplementedError


class MotorController:
    """Motor controller with encoder-based position control."""
    
    # Maximum degrees per second for speed = 100
    MAX_DEG_PER_SEC = 1080
    
    def __init__(self, hardware, positive_direction=1):
        """
        Initialize motor controller.
        
        Args:
            hardware: MotorHardware instance
            positive_direction: 1 or -1 to flip motor direction
        """
        self.hw = hardware
        self.positive_direction = positive_direction
    
    def get_angle(self):
        """Get current motor angle in degrees."""
        return self.hw.get_angle() * self.positive_direction
    
    def reset_angle(self, angle=0):
        """Reset motor angle to specified value."""
        self.hw.reset_angle(angle * self.positive_direction)
    
    def run(self, speed):
        """
        Run motor at specified speed.
        
        Args:
            speed: Speed in range -100 to 100
        """
        deg_s = speed * self.MAX_DEG_PER_SEC / 100
        self.hw.run(deg_s * self.positive_direction)
    
    def stop(self):
        """Stop the motor."""
        self.hw.stop()
    
    def hold(self):
        """Hold the motor at current position."""
        self.hw.hold()
    
    def drive_to_distance(self, distance_deg, speed=50, tolerance=5):
        """
        Drive motor to specified distance using encoder feedback.
        
        Args:
            distance_deg: Target distance in degrees relative to current position
            speed: Speed in range 0 to 100 (absolute value)
            tolerance: Position tolerance in degrees
        
        Returns:
            True if target reached, False if timed out
        """
        start_angle = self.get_angle()
        target_angle = start_angle + distance_deg
        
        # Determine direction
        direction = sign(distance_deg)
        if direction == 0:
            return True
        
        # Run motor toward target
        self.run(direction * abs(speed))
        
        # Wait until target is reached
        max_iterations = 1000
        for _ in range(max_iterations):
            current_angle = self.get_angle()
            error = target_angle - current_angle
            
            if abs(error) < tolerance:
                self.hold()
                return True
            
            # Check if we overshot
            if direction * error < 0:
                self.hold()
                return True
        
        # Timeout
        self.hold()
        return False
