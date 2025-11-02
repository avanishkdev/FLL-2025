"""
Mission 9 Pull - Refactored to use DriveController.

This mission performs the same sequence as the original mission_9_pull.py
but uses DriveController primitives for better closed-loop control.
"""

from robot.motors import MotorController
from robot.navigation import DriveController
from robot.pybricks_adapters import create_spike_prime_robot


def run_mission_9_pull():
    """
    Execute Mission 9 Pull using DriveController.
    
    Original sequence from mission_9_pull.py:
    - straight(180)
    - turn(-85)
    - straight(590)
    - turn(140)
    - straight(150)
    - left_gear.run_angle(1000, 650)
    - turn(-20)
    - straight(-150)
    - left_gear.run_angle(1000, -650)
    - turn(-130)
    - straight(-500)
    """
    # Create robot hardware
    robot = create_spike_prime_robot(wheel_diameter_mm=56, wheel_base_mm=80, ticks_per_rev=360)
    
    # Create motor controllers
    left_controller = MotorController(robot['left_hw'])
    right_controller = MotorController(robot['right_hw'])
    
    # Create drive controller
    drive = DriveController(
        left_motor=left_controller,
        right_motor=right_controller,
        gyro=robot['gyro'],
        wheel_diameter_mm=56,
        wheel_base_mm=80,
        ticks_per_rev=360
    )
    
    # Reset all sensors
    drive.reset()
    
    # Execute mission sequence
    # Set base speed to match original (400 mm/s => ~50% power)
    base_speed = 50
    turn_speed = 40
    
    # Step 1: Drive straight 180mm
    drive.drive_straight(180, speed=base_speed)
    
    # Step 2: Turn to -85 degrees (relative turn)
    current_heading = drive.gyro.get_angle()
    drive.turn_to(current_heading - 85, speed=turn_speed)
    
    # Step 3: Drive straight 590mm
    drive.drive_straight(590, speed=base_speed)
    
    # Step 4: Turn 140 degrees relative
    current_heading = drive.gyro.get_angle()
    drive.turn_to(current_heading + 140, speed=turn_speed)
    
    # Step 5: Drive straight 150mm
    drive.drive_straight(150, speed=base_speed)
    
    # Step 6: Run left gear motor
    robot['left_gear'].run_angle(1000, 650)
    
    # Step 7: Turn -20 degrees relative
    current_heading = drive.gyro.get_angle()
    drive.turn_to(current_heading - 20, speed=turn_speed)
    
    # Step 8: Drive straight -150mm (backward)
    drive.drive_straight(-150, speed=base_speed)
    
    # Step 9: Run left gear motor reverse
    robot['left_gear'].run_angle(1000, -650)
    
    # Step 10: Turn -130 degrees relative
    current_heading = drive.gyro.get_angle()
    drive.turn_to(current_heading - 130, speed=turn_speed)
    
    # Step 11: Drive straight -500mm (backward)
    drive.drive_straight(-500, speed=base_speed)
    
    # Mission complete - stop all motors
    drive.left_motor.hw.stop()
    drive.right_motor.hw.stop()
