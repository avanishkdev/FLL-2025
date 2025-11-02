"""
Motor controller with encoder-based distance control.
"""

from robot.utils import clamp


class MotorHardware:
    """
    Abstract interface for motor hardware.
    Concrete implementations should provide methods for setting power,
    reading encoders, and resetting encoders.
    """
    
    def set_power(self, power):
        """Set motor power (-100 to 100)."""
        raise NotImplementedError
    
    def get_angle(self):
        """Get current encoder angle in degrees."""
        raise NotImplementedError
    
    def reset_angle(self, angle=0):
        """Reset encoder to specified angle."""
        raise NotImplementedError
    
    def stop(self):
        """Stop the motor."""
        raise NotImplementedError


class MotorController:
    """
    Motor controller that uses encoder feedback to drive to a target distance.
    Exposes .hw attribute for use by higher-level controllers.
    """
    
    def __init__(self, hardware, ticks_per_mm=1.0):
        """
        Initialize motor controller.
        
        Args:
            hardware: MotorHardware instance
            ticks_per_mm: Encoder ticks per millimeter of travel
        """
        self.hw = hardware
        self.ticks_per_mm = ticks_per_mm
    
    def drive_to_distance(self, distance_mm, speed=50, tolerance=5):
        """
        Drive to a target distance using encoder feedback.
        
        Args:
            distance_mm: Target distance in millimeters
            speed: Base speed (0-100)
            tolerance: Distance tolerance in millimeters
        
        Returns:
            True if target reached within tolerance
        """
        target_ticks = distance_mm * self.ticks_per_mm
        self.hw.reset_angle(0)
        
        while True:
            current_ticks = self.hw.get_angle()
            error = target_ticks - current_ticks
            
            if abs(error) < tolerance * self.ticks_per_mm:
                self.hw.stop()
                return True
            
            # Simple proportional control
            power = clamp(error / 10.0, -speed, speed)
            self.hw.set_power(power)
    
    def reset_encoder(self):
        """Reset the encoder to zero."""
        self.hw.reset_angle(0)
