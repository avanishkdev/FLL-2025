"""Motor hardware abstraction and control."""

from robot.utils import sign


class MotorHardware:
    """Interface for motor hardware."""
    
    def set_speed(self, deg_per_sec):
        """Set motor speed in degrees per second."""
        raise NotImplementedError
    
    def get_angle(self):
        """Get current motor angle in degrees."""
        raise NotImplementedError
    
    def reset_angle(self, angle=0):
        """Reset motor angle to specified value."""
        raise NotImplementedError
    
    def stop(self):
        """Stop the motor."""
        raise NotImplementedError


class MotorController:
    """Motor controller with encoder-based distance control."""
    
    MAX_DEG_PER_SEC = 1080  # Maximum degrees per second
    
    def __init__(self, hardware, ticks_per_rev=360):
        """
        Initialize motor controller.
        
        Args:
            hardware: MotorHardware instance
            ticks_per_rev: Encoder ticks per revolution
        """
        self.hw = hardware
        self.ticks_per_rev = ticks_per_rev
    
    def drive_to_distance(self, distance_deg, speed_percent, timeout_ms=5000):
        """
        Drive motor to specified distance using encoder feedback.
        
        Args:
            distance_deg: Distance to travel in degrees
            speed_percent: Speed as percentage (-100 to 100)
            timeout_ms: Timeout in milliseconds
            
        Returns:
            True if reached target, False if timed out
        """
        from robot.utils import Timer
        
        # Record start position
        start_angle = self.hw.get_angle()
        target_angle = start_angle + distance_deg
        
        # Convert speed percentage to deg/sec
        speed_deg_per_sec = (speed_percent / 100.0) * self.MAX_DEG_PER_SEC
        
        # Ensure speed has correct sign
        if sign(distance_deg) != sign(speed_deg_per_sec) and speed_deg_per_sec != 0:
            speed_deg_per_sec = -speed_deg_per_sec
        
        # Start motor
        self.hw.set_speed(speed_deg_per_sec)
        
        # Wait until target reached or timeout
        timer = Timer()
        while timer.time() < timeout_ms:
            current_angle = self.hw.get_angle()
            remaining = abs(target_angle - current_angle)
            
            if remaining < 5:  # Close enough threshold
                break
        
        # Stop motor
        self.hw.stop()
        
        # Check if we reached target
        final_angle = self.hw.get_angle()
        return abs(target_angle - final_angle) < 10
