"""
Missions 8, 5, 9, and 10 - FLL 2025
Refactored to use Robot helper for consistent movements (2025-11-01)

This mission script performs missions 8, 5, 9, and 10, involving multiple
manipulator actions and navigation sequences.

Port Wiring:
- Left motor: Port A (counterclockwise)
- Right motor: Port C (clockwise)
- Manipulator (left gear): Port B (clockwise)
- Wheel diameter: 56 mm
- Axle track: 80 mm

When executed, runs all four missions in sequence.
"""

from pybricks.parameters import Direction, Port, Stop
from robot_helpers import Robot


def mission_8_and_5():
    """
    Execute missions 8 and 5.
    
    Performs navigation with rapid manipulator cycling.
    """
    robot.precise_straight(332)
    
    # Rapid manipulator cycling
    for count in range(4):
        robot.manipulator.control.limits(acceleration=9000)
        robot.run_manipulator(8000, 580, brake=Stop.HOLD, wait_time=0)
        robot.run_manipulator(8000, -580, brake=Stop.HOLD, wait_time=0)
    
    robot.set_precision_mode()
    robot.precise_turn(-30)
    
    robot.set_travel_mode()
    robot.precise_straight(400)
    
    robot.set_precision_mode()
    robot.precise_turn(35)
    robot.precise_straight(80)
    robot.precise_turn(-35)
    robot.precise_turn(30)
    robot.precise_straight(-80)


def mission_9_push_black_lever():
    """
    Execute mission 9 - Push black lever.
    
    Navigates to and pushes the black lever.
    """
    robot.set_precision_mode()
    robot.precise_turn(-60)
    robot.precise_straight(250)
    robot.precise_turn(-20)
    robot.precise_straight(250)
    robot.precise_turn(-140)
    
    robot.set_travel_mode()
    robot.precise_straight(400)


def mission_10_bucket_2():
    """
    Execute mission 10 - Bucket 2.
    
    Performs bucket manipulation with gear movements.
    """
    robot.set_precision_mode()
    robot.precise_straight(-180)
    robot.precise_turn(20)
    
    # Manipulator actions
    robot.run_manipulator(1000, 700, brake=Stop.HOLD)
    robot.run_manipulator(1000, -700, brake=Stop.HOLD)


def coming_back_from_10_bucket():
    """
    Return home from mission 10 bucket.
    
    Navigates back to the starting position.
    """
    robot.set_travel_mode()
    robot.precise_turn(-60)
    robot.precise_straight(350)
    
    robot.set_precision_mode()
    robot.precise_turn(40)
    
    robot.set_travel_mode()
    robot.precise_straight(630)


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

mission_8_and_5()
mission_9_push_black_lever()
mission_10_bucket_2()
coming_back_from_10_bucket()
