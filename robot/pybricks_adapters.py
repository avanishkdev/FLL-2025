"""
Pybricks-specific hardware adapters for Spike Prime robot.
"""

from pybricks.parameters import Port, Direction
from pybricks.pupdevices import Motor
from pybricks.hubs import PrimeHub
from robot.motors import MotorHardware
from robot.navigation import GyroAdapter


class PybricksMotorHardware(MotorHardware):
    """
    Hardware adapter for Pybricks Motor.
    Maps power values (-100 to 100) to motor speed in deg/s.
    """
    
    MAX_DEG_PER_SEC = 1080
    
    def __init__(self, motor):
        """
        Initialize with a Pybricks Motor instance.
        
        Args:
            motor: pybricks.pupdevices.Motor instance
        """
        self.motor = motor
    
    def set_power(self, power):
        """Set motor power (-100 to 100)."""
        speed = int((power / 100.0) * self.MAX_DEG_PER_SEC)
        self.motor.run(speed)
    
    def get_angle(self):
        """Get current encoder angle in degrees."""
        return self.motor.angle()
    
    def reset_angle(self, angle=0):
        """Reset encoder to specified angle."""
        self.motor.reset_angle(angle)
    
    def stop(self):
        """Stop the motor."""
        self.motor.stop()


class PybricksGyroAdapter(GyroAdapter):
    """
    Gyro adapter for Pybricks PrimeHub IMU.
    """
    
    def __init__(self, hub):
        """
        Initialize with a PrimeHub instance.
        
        Args:
            hub: pybricks.hubs.PrimeHub instance
        """
        self.hub = hub
    
    def get_angle(self):
        """Get current heading in degrees."""
        return self.hub.imu.heading()
    
    def reset(self):
        """Reset gyro to zero."""
        self.hub.imu.reset_heading(0)


def create_spike_prime_robot(wheel_diameter_mm=56, wheel_base_mm=80, ticks_per_rev=360):
    """
    Create robot hardware configuration for Spike Prime with standard port mapping.
    
    Port mapping from mission_9_pull.py:
    - Left motor: Port.A with Direction.COUNTERCLOCKWISE
    - Right motor: Port.C with Direction.CLOCKWISE
    - Left gear (manipulator): Port.B with Direction.CLOCKWISE
    
    Args:
        wheel_diameter_mm: Wheel diameter in millimeters
        wheel_base_mm: Distance between wheels in millimeters
        ticks_per_rev: Encoder ticks per revolution
    
    Returns:
        Dictionary with initialized components:
        - 'hub': PrimeHub instance
        - 'left_motor': Motor instance
        - 'right_motor': Motor instance
        - 'left_gear': Motor instance (for manipulator)
        - 'left_hw': PybricksMotorHardware for left motor
        - 'right_hw': PybricksMotorHardware for right motor
        - 'gyro': PybricksGyroAdapter instance
    """
    # Initialize hardware
    hub = PrimeHub()
    left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
    right_motor = Motor(Port.C, Direction.CLOCKWISE)
    left_gear = Motor(Port.B, Direction.CLOCKWISE)
    
    # Create adapters
    left_hw = PybricksMotorHardware(left_motor)
    right_hw = PybricksMotorHardware(right_motor)
    gyro = PybricksGyroAdapter(hub)
    
    return {
        'hub': hub,
        'left_motor': left_motor,
        'right_motor': right_motor,
        'left_gear': left_gear,
        'left_hw': left_hw,
        'right_hw': right_hw,
        'gyro': gyro,
    }
