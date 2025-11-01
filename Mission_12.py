"""
Mission 12 - FLL 2025
Refactored to use Robot helper for consistent movements (2025-11-01)

This mission script performs mission 12 with pull and push operations.

Port Wiring:
- Left motor (left-wheel): Port A (counterclockwise)
- Right motor (right-wheel): Port C (clockwise)
- Manipulator (left-gear): Port B (clockwise)
- Wheel diameter: 56 mm
- Axle track: 80 mm

When executed, runs mission_12() function.
"""

from pybricks.parameters import Direction, Port, Stop
from robot_helpers import Robot


def mission_12():
    """
    Execute mission 12 - Pull and push operations.
    
    Performs navigation with manipulator pull and push actions.
    Assumes robot starts at the designated starting position.
    """
    # Navigate to pull position
    robot.set_precision_mode()
    robot.precise_straight(62)
    robot.precise_turn(90)
    robot.precise_straight(260)
    
    # Pull operation
    robot.run_manipulator(300, 450, brake=Stop.HOLD)
    
    # Back up
    robot.drive.settings(straight_speed=300)
    robot.precise_straight(-125)
    
    # Release
    robot.run_manipulator(300, -425, brake=Stop.HOLD)
    
    # Navigate to push position
    robot.precise_turn(-90)
    robot.precise_straight(145)
    robot.precise_turn(90)
    
    # Push operation
    robot.drive.settings(straight_speed=220)
    robot.precise_straight(370)
    
    # Return
    robot.set_travel_mode()
    robot.precise_straight(-600)


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
mission_12()
