"""
Mission 7 - FLL 2025
Refactored to use Robot helper for consistent movements (2025-11-01)

This mission script performs mission 7 with manipulator operations and precise movements.

Port Wiring:
- Left motor: Port A (counterclockwise)
- Right motor: Port C (clockwise)
- Manipulator (left gear): Port B (clockwise)
- Wheel diameter: 56 mm
- Axle track: 80 mm

When executed, runs mission_7() function.
"""

from pybricks.parameters import Direction, Port, Stop
from pybricks.tools import wait
from robot_helpers import Robot


def mission_7():
    """
    Execute mission 7.
    
    Performs navigation with multiple manipulator actions and precise movements.
    Assumes robot starts at the designated starting position.
    """
    # Fast travel to mission area
    robot.set_travel_mode()
    robot.precise_straight(180)
    
    robot.set_precision_mode()
    robot.precise_turn(-85)
    robot.precise_straight(185)
    robot.precise_turn(85)
    
    # Continue travel
    robot.set_travel_mode()
    robot.precise_straight(420)
    
    robot.set_precision_mode()
    robot.precise_turn(60)
    robot.precise_straight(185)
    
    # Manipulator actions
    robot.run_manipulator(200, 450, brake=Stop.HOLD)
    robot.run_manipulator(200, -75, brake=Stop.HOLD)
    wait(2000)
    
    # Adjust position
    robot.set_custom_speed(straight_speed=200, turn_rate=100)
    robot.precise_turn(-36)
    wait(2000)
    robot.run_manipulator(200, -25, brake=Stop.HOLD)
    
    # More precise movements
    robot.precise_straight(-50)
    robot.run_manipulator(100, -150, brake=Stop.HOLD)
    robot.precise_turn(56)
    robot.precise_straight(-120)
    
    # Arc movement (using drive.arc directly)
    robot.drive.arc(140, angle=-170)
    wait(50)
    
    robot.precise_straight(-200)
    robot.precise_turn(-90)
    robot.run_manipulator(200, 300, brake=Stop.HOLD)


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
mission_7()
