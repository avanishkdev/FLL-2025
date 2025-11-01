"""
Robot Helper Module for FLL 2025
Refactored to use Robot helper for consistent movements (2025-11-01)

This module provides a Robot class that wraps DriveBase and Motor operations
for predictable, accurate movements with built-in settle delays.

Port Wiring:
- Left motor: Port A (counterclockwise)
- Right motor: Port C (clockwise)
- Manipulator: Port B (varies by robot configuration)
- Wheel diameter: 56 mm
- Axle track: 80 mm
"""

from pybricks.hubs import PrimeHub
from pybricks.parameters import Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import wait


class Robot:
    """
    High-level robot control class for FLL missions.
    
    Provides methods for precise movements with built-in settle delays,
    manipulator control, and mode switching for different movement types.
    """
    
    def __init__(self, left_port=Port.A, right_port=Port.C, manipulator_port=Port.B,
                 left_direction=Direction.COUNTERCLOCKWISE, right_direction=Direction.CLOCKWISE,
                 manipulator_direction=Direction.CLOCKWISE,
                 wheel_diameter=56, axle_track=80):
        """
        Initialize the robot with motors and drivebase.
        
        Args:
            left_port: Port for left motor (default Port.A)
            right_port: Port for right motor (default Port.C)
            manipulator_port: Port for manipulator motor (default Port.B)
            left_direction: Direction for left motor (default COUNTERCLOCKWISE)
            right_direction: Direction for right motor (default CLOCKWISE)
            manipulator_direction: Direction for manipulator motor (default CLOCKWISE)
            wheel_diameter: Wheel diameter in mm (default 56)
            axle_track: Distance between wheels in mm (default 80)
        """
        self.hub = PrimeHub()
        self.left_motor = Motor(left_port, left_direction)
        self.right_motor = Motor(right_port, right_direction)
        self.manipulator = Motor(manipulator_port, manipulator_direction)
        self.drive = DriveBase(self.left_motor, self.right_motor, wheel_diameter, axle_track)
        
        # Default settings
        self.drive.use_gyro(True)
        self.settle_time = 50  # Default settle time in ms
        
    def set_precision_mode(self):
        """
        Set drive settings for precision movements.
        Use before precise maneuvers, turns, or short distances.
        """
        self.drive.settings(straight_speed=200, straight_acceleration=100,
                           turn_rate=100, turn_acceleration=50)
        
    def set_travel_mode(self):
        """
        Set drive settings for fast travel over long distances.
        Use before long straight movements (> 400 mm).
        """
        self.drive.settings(straight_speed=500, straight_acceleration=300,
                           turn_rate=200, turn_acceleration=100)
    
    def precise_straight(self, distance_mm, speed=None):
        """
        Drive straight with precision and settle wait.
        
        Args:
            distance_mm: Distance to travel in millimeters (negative for backward)
            speed: Optional speed override in mm/s
        """
        if speed is not None:
            old_speed = self.drive.settings()['straight_speed']
            self.drive.settings(straight_speed=speed)
            self.drive.straight(distance_mm)
            self.drive.settings(straight_speed=old_speed)
        else:
            self.drive.straight(distance_mm)
        wait(self.settle_time)
    
    def precise_turn(self, angle_deg, turn_rate=None):
        """
        Turn with precision and settle wait.
        
        Args:
            angle_deg: Angle to turn in degrees (positive=left, negative=right)
            turn_rate: Optional turn rate override in deg/s
        """
        if turn_rate is not None:
            old_rate = self.drive.settings()['turn_rate']
            self.drive.settings(turn_rate=turn_rate)
            self.drive.turn(angle_deg)
            self.drive.settings(turn_rate=old_rate)
        else:
            self.drive.turn(angle_deg)
        wait(self.settle_time)
    
    def run_manipulator(self, speed, angle, brake=Stop.BRAKE, wait_time=100):
        """
        Run the manipulator motor with settle wait.
        
        Args:
            speed: Speed in deg/s
            angle: Angle to rotate in degrees
            brake: Stop behavior (Stop.BRAKE, Stop.HOLD, Stop.COAST)
            wait_time: Time to wait after movement in ms (default 100)
        """
        self.manipulator.run_angle(speed, angle, then=brake, wait=True)
        wait(wait_time)
    
    def reset_manipulator_angle(self, angle=0):
        """
        Reset the manipulator motor angle.
        
        Args:
            angle: Angle to reset to (default 0)
        """
        self.manipulator.reset_angle(angle)
    
    def reset_drive(self, distance=0, angle=0):
        """
        Reset the drivebase distance and heading.
        
        Args:
            distance: Distance to reset to in mm (default 0)
            angle: Angle to reset to in degrees (default 0)
        """
        self.drive.reset(distance, angle)
        
    def reset_left_motor_angle(self, angle=0):
        """
        Reset the left motor angle.
        
        Args:
            angle: Angle to reset to (default 0)
        """
        self.left_motor.reset_angle(angle)
