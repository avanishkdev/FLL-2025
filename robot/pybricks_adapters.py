"""Pybricks hardware adapters for robot control framework."""

from pybricks.parameters import Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.hubs import PrimeHub
from robot.motors import MotorHardware, MotorController
from robot.navigation import GyroAdapter


class PybricksMotorHardware(MotorHardware):
    """Pybricks Motor hardware adapter."""
    
    def __init__(self, motor):
        """
        Initialize Pybricks motor hardware.
        
        Args:
            motor: Pybricks Motor instance
        """
        self.motor = motor
    
    def get_angle(self):
        """Get current motor angle in degrees."""
        return self.motor.angle()
    
    def reset_angle(self, angle=0):
        """Reset motor angle to specified value."""
        self.motor.reset_angle(angle)
    
    def run(self, speed):
        """Run motor at specified speed (deg/s)."""
        self.motor.run(speed)
    
    def stop(self):
        """Stop the motor."""
        self.motor.stop()
    
    def hold(self):
        """Hold the motor at current position."""
        self.motor.hold()


class PybricksGyroAdapter(GyroAdapter):
    """Pybricks gyro adapter using Prime Hub IMU."""
    
    def __init__(self, hub):
        """
        Initialize Pybricks gyro adapter.
        
        Args:
            hub: Pybricks PrimeHub instance
        """
        self.hub = hub
    
    def get_heading(self):
        """Get current heading in degrees."""
        return self.hub.imu.heading()
    
    def reset_heading(self, angle=0):
        """Reset heading to specified angle."""
        self.hub.imu.reset_heading(angle)


def create_robot_from_mission_9_config():
    """
    Create robot configuration matching mission_9_pull.py hardware setup.
    
    Returns:
        Tuple of (left_motor_controller, right_motor_controller, gyro_adapter, manipulator_motor)
    """
    # Initialize hardware
    prime_hub = PrimeHub()
    
    # Motors matching mission_9_pull.py configuration
    right_motor_hw = Motor(Port.C, Direction.CLOCKWISE)
    left_motor_hw = Motor(Port.A, Direction.COUNTERCLOCKWISE)
    manipulator = Motor(Port.B, Direction.CLOCKWISE)
    
    # Create hardware adapters
    right_hw = PybricksMotorHardware(right_motor_hw)
    left_hw = PybricksMotorHardware(left_motor_hw)
    gyro = PybricksGyroAdapter(prime_hub)
    
    # Create motor controllers with direction mapping
    # Right motor: Port.C, Direction.CLOCKWISE -> positive_direction=1
    right_controller = MotorController(right_hw, positive_direction=1)
    
    # Left motor: Port.A, Direction.COUNTERCLOCKWISE -> positive_direction=-1
    # This reverses the direction to match the original mission behavior
    left_controller = MotorController(left_hw, positive_direction=-1)
    
    return left_controller, right_controller, gyro, manipulator
