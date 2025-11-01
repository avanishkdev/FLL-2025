"""Pybricks hardware adapters for robot control."""

from pybricks.hubs import PrimeHub
from pybricks.parameters import Direction, Port
from pybricks.pupdevices import Motor
from robot.motors import MotorController
from robot.navigation import DriveController


# Constants from mission_9_pull.py configuration
MAX_DEG_PER_SEC = 1080
TICKS_PER_REV = 360
WHEEL_DIAMETER_MM = 56
WHEEL_BASE_MM = 80


def create_robot_from_mission_9_config():
    """
    Create robot hardware adapters matching mission_9_pull.py configuration.
    
    Hardware setup from mission_9_pull.py:
    - left motor: Port.A, Direction.COUNTERCLOCKWISE (positive_direction=-1)
    - right motor: Port.C, Direction.CLOCKWISE (positive_direction=1)
    - left_gear: Port.B, Direction.CLOCKWISE
    - wheel_diameter: 56mm
    - wheel_base: 80mm
    
    Returns:
        dict with keys: hub, left_motor, right_motor, left_gear, drive_controller
    """
    # Initialize hardware
    hub = PrimeHub()
    
    # Create motors matching mission_9_pull.py configuration
    left_hw = Motor(Port.A, Direction.COUNTERCLOCKWISE)
    right_hw = Motor(Port.C, Direction.CLOCKWISE)
    left_gear_hw = Motor(Port.B, Direction.CLOCKWISE)
    
    # Wrap in MotorControllers
    # Left motor: COUNTERCLOCKWISE direction means positive_direction=-1
    left_motor = MotorController(
        motor=left_hw,
        positive_direction=-1,
        ticks_per_rev=TICKS_PER_REV,
        max_speed=100,
        max_deg_per_sec=MAX_DEG_PER_SEC
    )
    
    # Right motor: CLOCKWISE direction means positive_direction=1
    right_motor = MotorController(
        motor=right_hw,
        positive_direction=1,
        ticks_per_rev=TICKS_PER_REV,
        max_speed=100,
        max_deg_per_sec=MAX_DEG_PER_SEC
    )
    
    # Create drive controller
    drive_controller = DriveController(
        left_motor=left_motor,
        right_motor=right_motor,
        gyro=hub.imu,
        wheel_diameter_mm=WHEEL_DIAMETER_MM,
        wheel_base_mm=WHEEL_BASE_MM,
        ticks_per_rev=TICKS_PER_REV,
        max_speed=100
    )
    
    return {
        'hub': hub,
        'left_motor': left_motor,
        'right_motor': right_motor,
        'left_gear': left_gear_hw,
        'drive_controller': drive_controller
    }
