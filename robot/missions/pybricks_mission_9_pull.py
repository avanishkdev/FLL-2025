"""Mission 9 Pull - Refactored using DriveController primitives."""

from robot.pybricks_adapters import create_robot_from_mission_9_config


def run():
    """
    Execute Mission 9 Pull using DriveController primitives.
    
    Original sequence from mission_9_pull.py:
    1. drive_base.settings(straight_speed=400)
    2. drive_base.straight(180)
    3. drive_base.turn(-85)
    4. drive_base.straight(590)
    5. drive_base.turn(140)
    6. drive_base.straight(150)
    7. left_gear.run_angle(1000, 650)
    8. drive_base.turn(-20)
    9. drive_base.straight(-150)
    10. left_gear.run_angle(1000, -650)
    11. drive_base.turn(-130)
    12. drive_base.straight(-500)
    """
    # Create robot hardware
    robot = create_robot_from_mission_9_config()
    drive = robot['drive_controller']
    left_gear = robot['left_gear']
    hub = robot['hub']
    
    # Reset/initialize
    hub.imu.reset_heading(0)
    drive.reset()
    
    # Execute mission sequence
    # Step 1: Drive forward 180mm
    drive.drive_straight(180, speed=40)
    
    # Step 2: Turn -85 degrees (turn left)
    current_heading = hub.imu.angle()
    drive.turn_to(current_heading - 85, speed=50)
    
    # Step 3: Drive forward 590mm
    drive.drive_straight(590, speed=40)
    
    # Step 4: Turn 140 degrees (turn right)
    current_heading = hub.imu.angle()
    drive.turn_to(current_heading + 140, speed=50)
    
    # Step 5: Drive forward 150mm
    drive.drive_straight(150, speed=40)
    
    # Step 6: Operate left gear (deploy mechanism)
    left_gear.run_angle(1000, 650, wait=True)
    
    # Step 7: Turn -20 degrees (turn left slightly)
    current_heading = hub.imu.angle()
    drive.turn_to(current_heading - 20, speed=50)
    
    # Step 8: Drive backward 150mm
    drive.drive_straight(-150, speed=40)
    
    # Step 9: Operate left gear (retract mechanism)
    left_gear.run_angle(1000, -650, wait=True)
    
    # Step 10: Turn -130 degrees (turn left)
    current_heading = hub.imu.angle()
    drive.turn_to(current_heading - 130, speed=50)
    
    # Step 11: Drive backward 500mm
    drive.drive_straight(-500, speed=40)
