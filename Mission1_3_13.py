"""
Mission 1, 3, and 13 - FLL 2025
Refactored to use Robot helper for consistent movements (2025-11-01)

This mission script performs missions 1, 3, and 13, involving statue rebuild,
mineshaft operations, and various manipulator movements.

Port Wiring:
- Left motor: Port A (counterclockwise)
- Right motor: Port C (clockwise)
- Left gear manipulator: Port B (counterclockwise)
- Right gear manipulator: Port D (counterclockwise)
- Wheel diameter: 56 mm
- Axle track: 80 mm (Note: Original used 98mm; standardized to 80mm per refactoring)

When executed, runs mission_1_3_13() function.
"""

from pybricks.parameters import Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.tools import wait
from robot_helpers import Robot


def mission_1_3_13():
    """
    Execute missions 1, 3, and 13.
    
    Performs statue rebuild (mission 13), mineshaft operations (mission 3),
    and returns home. Uses both left and right gear manipulators.
    Assumes robot starts at the designated starting position.
    """
    # Move towards mission 13 - Statue rebuild
    robot.drive.settings(straight_speed=300)
    robot.set_travel_mode()
    robot.precise_straight(850)
    
    robot.set_precision_mode()
    robot.precise_turn(110)
    robot.precise_straight(195)
    robot.precise_turn(40)
    robot.precise_straight(110)
    robot.precise_turn(-10)
    robot.reset_left_motor_angle(0)
    
    # Reached mission 13 - Statue rebuild - Lift arm
    robot.precise_turn(-7)
    robot.run_manipulator(300, 250, brake=Stop.HOLD)
    robot.precise_turn(7)
    
    # Mission 13 complete - Move back
    robot.precise_straight(-195)
    robot.run_manipulator(300, -250, brake=Stop.HOLD)
    robot.precise_turn(-62)
    robot.run_manipulator(1000, 375, brake=Stop.HOLD)
    wait(1000)
    
    # Mission 3 - Mineshaft complete - Lower arm and move back home
    robot.run_manipulator(1000, -360, brake=Stop.HOLD)
    robot.reset_manipulator_angle(0)
    robot.precise_straight(-100)
    robot.run_manipulator(1000, 360, brake=Stop.HOLD)
    robot.precise_turn(100)
    robot.precise_straight(220)
    robot.precise_turn(90)
    
    # Use right gear manipulator
    right_gear.reset_angle(0)
    right_gear.run_angle(1000, 455, then=Stop.HOLD, wait=True)
    wait(100)
    
    robot.drive.settings(straight_speed=100)
    robot.precise_straight(120)
    right_gear.reset_angle(0)
    right_gear.run_angle(500, -100, then=Stop.HOLD, wait=True)
    wait(100)
    
    robot.precise_turn(-90)
    robot.set_travel_mode()
    robot.precise_straight(500)


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

# Additional motor for right gear
right_gear = Motor(Port.D, Direction.COUNTERCLOCKWISE)

# The main program starts here.
mission_1_3_13()
