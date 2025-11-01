"""
Mission 10 - Pull - FLL 2025
Refactored to use Robot helper for consistent movements (2025-11-01)

This mission script performs mission 10 with pull operations using the manipulator.

Port Wiring:
- Left motor: Port A (counterclockwise)
- Right motor: Port C (clockwise)
- Manipulator (left gear): Port B (clockwise)
- Wheel diameter: 56 mm
- Axle track: 80 mm

When executed, runs mission_10_pull() function.
"""

from pybricks.parameters import Direction, Port, Stop
from robot_helpers import Robot


def mission_10_pull():
    """
    Execute mission 10 - Pull operation.
    
    Performs navigation with manipulator pull actions and arc movement.
    Assumes robot starts at the designated starting position.
    """
    # Navigate to mission area
    robot.set_precision_mode()
    robot.precise_straight(180)
    robot.precise_turn(-85)
    
    robot.set_travel_mode()
    robot.precise_straight(340)
    
    robot.set_precision_mode()
    robot.precise_turn(50)
    robot.precise_straight(133)
    
    # Pull operation
    robot.run_manipulator(1000, 650, brake=Stop.HOLD)
    
    # Arc movement (using drive.arc directly)
    robot.drive.arc(100, angle=-50)
    robot.set_settle_time(50)
    
    # Return
    robot.set_travel_mode()
    robot.precise_straight(-500)
    
    # Release
    robot.run_manipulator(1000, -650, brake=Stop.HOLD)


# Set up robot with standard configuration
robot = Robot(
    left_port=Port.A,
    right_port=Port.C,
    manipulator_port=Port.B,
    left_direction=Direction.COUNTERCLOCKWISE,
    right_direction=Direction.CLOCKWISE,
    manipulator_direction=Direction.CLOCKWISE,
    wheel_diameter=56,
    axle_track=80
)

# The main program starts here.
robot.reset_drive(0, 0)
robot.reset_left_motor_angle(0)
mission_10_pull()
