"""Refactored Mission 9 Pull using DriveController and Pybricks adapters."""

from robot.motors import MotorController
from robot.navigation import DriveController
from robot.pybricks_adapters import create_pybricks_hardware


def run_mission_9_pull():
    """
    Execute Mission 9 Pull sequence using DriveController.
    
    Sequence (from original mission_9_pull.py):
    1. Drive straight 180mm
    2. Turn -85 degrees
    3. Drive straight 590mm
    4. Turn 140 degrees
    5. Drive straight 150mm
    6. Manipulator: left_gear.run_angle(1000, 650)
    7. Turn -20 degrees
    8. Drive straight -150mm
    9. Manipulator: left_gear.run_angle(1000, -650)
    10. Turn -130 degrees
    11. Drive straight -500mm
    """
    # Create hardware
    hw = create_pybricks_hardware()
    
    # Reset encoders and gyro
    hw['right_motor'].reset_angle(0)
    hw['left_motor'].reset_angle(0)
    hw['gyro'].reset()
    
    # Create motor controllers
    right_controller = MotorController(hw['right_motor'], ticks_per_rev=hw['ticks_per_rev'])
    left_controller = MotorController(hw['left_motor'], ticks_per_rev=hw['ticks_per_rev'])
    
    # Create drive controller with tuned PID parameters
    drive = DriveController(
        left_motor=left_controller,
        right_motor=right_controller,
        gyro=hw['gyro'],
        wheel_diameter_mm=hw['wheel_diameter_mm'],
        wheel_base_mm=hw['wheel_base_mm'],
        heading_kp=2.0,
        heading_ki=0.1,
        heading_kd=0.5
    )
    
    # Default speeds (tuned for robot)
    drive_speed = 50  # Base speed for driving
    turn_speed = 30   # Base speed for turning
    
    # Execute mission sequence
    # 1. Drive straight 180mm
    drive.drive_straight(180, base_speed=drive_speed, timeout_ms=5000)
    
    # 2. Turn to -85 degrees (relative to start)
    current_heading = hw['gyro'].get_angle()
    target_heading = current_heading - 85
    drive.turn_to(target_heading, max_speed=turn_speed, timeout_ms=3000)
    
    # 3. Drive straight 590mm
    drive.drive_straight(590, base_speed=drive_speed, timeout_ms=8000)
    
    # 4. Turn 140 degrees (relative to previous heading)
    current_heading = hw['gyro'].get_angle()
    target_heading = current_heading + 140
    drive.turn_to(target_heading, max_speed=turn_speed, timeout_ms=5000)
    
    # 5. Drive straight 150mm
    drive.drive_straight(150, base_speed=drive_speed, timeout_ms=5000)
    
    # 6. Manipulator action: left_gear.run_angle(1000, 650)
    hw['left_gear'].run_angle(1000, 650)
    
    # 7. Turn -20 degrees (relative to previous heading)
    current_heading = hw['gyro'].get_angle()
    target_heading = current_heading - 20
    drive.turn_to(target_heading, max_speed=turn_speed, timeout_ms=3000)
    
    # 8. Drive straight -150mm (backward)
    drive.drive_straight(-150, base_speed=drive_speed, timeout_ms=5000)
    
    # 9. Manipulator action: left_gear.run_angle(1000, -650)
    hw['left_gear'].run_angle(1000, -650)
    
    # 10. Turn -130 degrees (relative to previous heading)
    current_heading = hw['gyro'].get_angle()
    target_heading = current_heading - 130
    drive.turn_to(target_heading, max_speed=turn_speed, timeout_ms=5000)
    
    # 11. Drive straight -500mm (backward)
    drive.drive_straight(-500, base_speed=drive_speed, timeout_ms=8000)
