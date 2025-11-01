"""
Mission 9 - Pull - FLL 2025
Refactored to use Robot helper for consistent movements (2025-11-01)

This mission script performs mission 9 with pull operations using the manipulator.

Port Wiring:
- Left motor: Port A (counterclockwise)
- Right motor: Port C (clockwise)
- Manipulator (left gear): Port B (clockwise)
- Wheel diameter: 56 mm
- Axle track: 80 mm

When executed, runs mission_9_pull() function.
"""

from pybricks.parameters import Direction, Port, Stop
from robot_helpers import Robot


def mission_9_pull():
    """
    Execute mission 9 - Pull operation.
    
    Performs navigation with manipulator pull and push actions.
    Assumes robot starts at the designated starting position.
    """
    # Navigate to mission area
    robot.set_travel_mode()
    robot.precise_straight(180)
    
    robot.set_precision_mode()
    robot.precise_turn(-85)
    
    robot.set_travel_mode()
    robot.precise_straight(590)
    
    robot.set_precision_mode()
    robot.precise_turn(140)
    robot.precise_straight(150)
    
    # Pull operation
    robot.run_manipulator(1000, 650, brake=Stop.HOLD)
    
    robot.precise_turn(-20)
    robot.precise_straight(-150)
    
    # Release
    robot.run_manipulator(1000, -650, brake=Stop.HOLD)
    
    robot.precise_turn(-130)
    
    # Return
    robot.set_travel_mode()
    robot.precise_straight(-500)


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
mission_9_pull()
