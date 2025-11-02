"""Refactored Mission 9 Pull using DriveController and navigation primitives."""

from robot.pybricks_adapters import create_robot_from_mission_9_config
from robot.navigation import DriveController


def run_mission_9_pull():
    """
    Execute Mission 9 Pull sequence using DriveController.
    
    This mission performs the same sequence as the original mission_9_pull.py:
    1. Drive straight 180mm
    2. Turn -85 degrees
    3. Drive straight 590mm
    4. Turn 140 degrees
    5. Drive straight 150mm
    6. Manipulator up (650 deg at 1000 deg/s)
    7. Turn -20 degrees
    8. Drive straight -150mm
    9. Manipulator down (-650 deg at 1000 deg/s)
    10. Turn -130 degrees
    11. Drive straight -500mm
    """
    # Create robot hardware
    left_motor, right_motor, gyro, manipulator = create_robot_from_mission_9_config()
    
    # Create drive controller with mission_9_pull specifications
    drive = DriveController(
        left_motor, 
        right_motor, 
        gyro,
        wheel_diameter_mm=56,
        wheel_base_mm=80
    )
    
    # Reset encoders and gyro
    drive.reset()
    
    # Mission sequence with tuned speeds and timeouts
    
    # Step 1: Drive forward 180mm
    drive.drive_straight(180, base_speed=50, timeout_ms=5000)
    
    # Step 2: Turn left 85 degrees (target heading = -85)
    current_heading = gyro.get_heading()
    drive.turn_to(current_heading - 85, timeout_ms=5000)
    
    # Step 3: Drive forward 590mm
    drive.drive_straight(590, base_speed=50, timeout_ms=8000)
    
    # Step 4: Turn right 140 degrees (target heading = current + 140)
    current_heading = gyro.get_heading()
    drive.turn_to(current_heading + 140, timeout_ms=5000)
    
    # Step 5: Drive forward 150mm
    drive.drive_straight(150, base_speed=50, timeout_ms=5000)
    
    # Step 6: Manipulator up
    manipulator.run_angle(1000, 650)
    
    # Step 7: Turn left 20 degrees
    current_heading = gyro.get_heading()
    drive.turn_to(current_heading - 20, timeout_ms=5000)
    
    # Step 8: Drive backward 150mm
    drive.drive_straight(-150, base_speed=50, timeout_ms=5000)
    
    # Step 9: Manipulator down
    manipulator.run_angle(1000, -650)
    
    # Step 10: Turn left 130 degrees
    current_heading = gyro.get_heading()
    drive.turn_to(current_heading - 130, timeout_ms=5000)
    
    # Step 11: Drive backward 500mm
    drive.drive_straight(-500, base_speed=50, timeout_ms=8000)
