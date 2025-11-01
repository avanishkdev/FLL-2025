"""
Mission 1 and 2 - FLL 2025
Refactored to use Robot helper for consistent movements (2025-11-01)

This mission script performs missions 1 and 2, involving turns, straight movements,
and manipulator operations.

Port Wiring:
- Left motor: Port A (counterclockwise)
- Right motor: Port C (clockwise)
- Manipulator (left gear): Port B (counterclockwise)
- Wheel diameter: 56 mm
- Axle track: 80 mm (Note: Original used 98mm; standardized to 80mm per refactoring)

When executed, runs mission_1_and_2() function.
"""

from pybricks.parameters import Direction, Port, Stop
from robot_helpers import Robot


def mission_1_and_2():
    """
    Execute missions 1 and 2.
    
    Performs a sequence of turns, straight movements, and manipulator actions.
    Assumes robot starts at the designated starting position.
    """
    # Set precision mode for accurate movements
    robot.set_precision_mode()
    
    # Navigate to mission area
    robot.precise_turn(-40)
    robot.precise_straight(250)
    robot.precise_turn(40)
    
    # Long travel to mission location
    robot.set_travel_mode()
    robot.precise_straight(550)
    
    # Manipulator action
    robot.run_manipulator(300, 180, brake=Stop.BRAKE)
    
    # Navigate around obstacles
    robot.set_precision_mode()
    robot.precise_turn(-45)
    robot.precise_straight(150)
    robot.precise_straight(-130)
    robot.precise_turn(45)
    
    # Return home
    robot.set_travel_mode()
    robot.precise_straight(-700)


# Set up robot with standard configuration
robot = Robot(
    left_port=Port.A,
    right_port=Port.C,
    manipulator_port=Port.B,
    left_direction=Direction.COUNTERCLOCKWISE,
    right_direction=Direction.CLOCKWISE,
    manipulator_direction=Direction.COUNTERCLOCKWISE,
    wheel_diameter=56,
    axle_track=80
)

# The main program starts here.
mission_1_and_2()
