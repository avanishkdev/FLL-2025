"""Pybricks hardware adapters for robot control."""

from pybricks.parameters import Direction, Port
from pybricks.pupdevices import Motor
from pybricks.hubs import PrimeHub
from robot.motors import MotorHardware


class PybricksMotorHardware(MotorHardware):
    """Pybricks motor hardware adapter."""
    
    def __init__(self, motor, positive_direction=1):
        """
        Initialize Pybricks motor hardware.
        
        Args:
            motor: Pybricks Motor instance
            positive_direction: 1 for normal, -1 for reversed
        """
        self.motor = motor
        self.positive_direction = positive_direction
    
    def set_speed(self, deg_per_sec):
        """Set motor speed in degrees per second."""
        self.motor.run(deg_per_sec * self.positive_direction)
    
    def get_angle(self):
        """Get current motor angle in degrees."""
        return self.motor.angle() * self.positive_direction
    
    def reset_angle(self, angle=0):
        """Reset motor angle to specified value."""
        self.motor.reset_angle(angle * self.positive_direction)
    
    def stop(self):
        """Stop the motor."""
        self.motor.stop()


class PybricksGyroAdapter:
    """Pybricks gyro adapter."""
    
    def __init__(self, hub):
        """
        Initialize Pybricks gyro adapter.
        
        Args:
            hub: PrimeHub instance
        """
        self.hub = hub
    
    def get_angle(self):
        """Get current gyro heading in degrees."""
        return self.hub.imu.heading()
    
    def reset(self):
        """Reset gyro heading to 0."""
        self.hub.imu.reset_heading(0)


def create_pybricks_hardware():
    """
    Create Pybricks hardware instances with correct port mappings from mission_9_pull.py.
    
    Port mappings:
    - right motor: Port.C, Direction.CLOCKWISE (positive_direction=1)
    - left motor: Port.A, Direction.COUNTERCLOCKWISE (positive_direction=-1)
    - left_gear: Port.B (manipulator)
    
    Returns:
        Dictionary with hardware instances
    """
    # Initialize hardware
    prime_hub = PrimeHub()
    
    # Create motors with correct directions
    right_motor_hw = Motor(Port.C, Direction.CLOCKWISE)
    left_motor_hw = Motor(Port.A, Direction.COUNTERCLOCKWISE)
    left_gear = Motor(Port.B, Direction.CLOCKWISE)
    
    # Create adapters
    # Note: left motor uses Direction.COUNTERCLOCKWISE in mission_9_pull,
    # so we reverse it with positive_direction=-1
    right_adapter = PybricksMotorHardware(right_motor_hw, positive_direction=1)
    left_adapter = PybricksMotorHardware(left_motor_hw, positive_direction=-1)
    
    # Create gyro adapter
    gyro = PybricksGyroAdapter(prime_hub)
    
    return {
        'prime_hub': prime_hub,
        'right_motor': right_adapter,
        'left_motor': left_adapter,
        'left_gear': left_gear,
        'gyro': gyro,
        'wheel_diameter_mm': 56,
        'wheel_base_mm': 80,
        'ticks_per_rev': 360
    }
