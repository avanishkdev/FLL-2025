"""
Mission 6 - Forge - FLL 2025
Refactored to use Robot helper for consistent movements (2025-11-01)

This mission script performs mission 6 (Forge), involving navigation and turns.

Port Wiring:
- Left motor: Port A (counterclockwise)
- Right motor: Port C (clockwise)
- Manipulator (left gear): Port B (clockwise)
- Wheel diameter: 56 mm
- Axle track: 80 mm

When executed, runs mission_6_forge() function.
"""

from pybricks.parameters import Direction, Port, Stop
from robot_helpers import Robot


def mission_6_forge():
    """
    Execute mission 6 - Forge.
    
    Performs navigation to and around the forge area with various turns.
    Assumes robot starts at the designated starting position.
    """
    # Fast travel to mission area
    robot.set_travel_mode()
    robot.precise_straight(180)
    
    robot.set_precision_mode()
    robot.precise_turn(-85)
    robot.precise_straight(185)
    robot.precise_turn(85)
    
    # Long travel
    robot.set_travel_mode()
    robot.precise_straight(450)
    
    # Navigate through mission area
    robot.set_precision_mode()
    robot.precise_turn(40)
    robot.precise_straight(80)
    robot.precise_turn(-60)
    robot.precise_turn(-85)
    robot.precise_straight(100)
    robot.precise_straight(-180)
    robot.precise_turn(20)
    robot.precise_straight(-200)
    robot.precise_straight(250)
    robot.precise_turn(-90)
    
    # Return travel
    robot.set_travel_mode()
    robot.precise_straight(500)


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
mission_6_forge()
