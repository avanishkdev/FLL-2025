"""Navigation controller for precise robot movement."""

import math
from robot.utils import clamp, trimmed_angle_deg, sign
from robot.pid import PID


class DriveController:
    """Drive controller for precise straight and turning movements."""
    
    def __init__(self, left_motor, right_motor, gyro, wheel_diameter_mm=56, 
                 wheel_base_mm=80, ticks_per_rev=360, max_speed=100):
        """
        Initialize drive controller.
        
        Args:
            left_motor: MotorController for left wheel
            right_motor: MotorController for right wheel
            gyro: Gyro sensor object (with angle() method)
            wheel_diameter_mm: Diameter of drive wheels in mm
            wheel_base_mm: Distance between wheels in mm
            ticks_per_rev: Encoder ticks per revolution
            max_speed: Maximum speed in numeric scale (-100 to 100)
        """
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.gyro = gyro
        self.wheel_diameter_mm = wheel_diameter_mm
        self.wheel_base_mm = wheel_base_mm
        self.ticks_per_rev = ticks_per_rev
        self.max_speed = max_speed
        
        # Calculate wheel circumference
        self.wheel_circumference = math.pi * wheel_diameter_mm
        
        # PID controllers for heading and distance
        self.heading_pid = PID(kp=1.5, ki=0.0, kd=0.1, integral_limit=20)
        self.distance_pid = PID(kp=0.5, ki=0.0, kd=0.0)
    
    def mm_to_ticks(self, distance_mm):
        """Convert millimeters to encoder ticks."""
        rotations = distance_mm / self.wheel_circumference
        return rotations * self.ticks_per_rev
    
    def ticks_to_mm(self, ticks):
        """Convert encoder ticks to millimeters."""
        rotations = ticks / self.ticks_per_rev
        return rotations * self.wheel_circumference
    
    def reset(self):
        """Reset encoders and gyro."""
        self.left_motor.reset_angle(0)
        self.right_motor.reset_angle(0)
        self.heading_pid.reset()
        self.distance_pid.reset()
    
    def turn_to(self, target_angle, speed=50, tolerance=2):
        """
        Turn to absolute heading using gyro.
        
        Args:
            target_angle: Target heading in degrees
            speed: Maximum turn speed (numeric scale)
            tolerance: Acceptable angle error in degrees
        """
        while True:
            current_angle = self.gyro.angle()
            error = trimmed_angle_deg(target_angle - current_angle)
            
            if abs(error) < tolerance:
                self.left_motor.stop()
                self.right_motor.stop()
                break
            
            # Simple proportional control for turning
            turn_speed = clamp(error * 0.8, -speed, speed)
            
            # Apply turn (left negative, right positive for clockwise)
            self.left_motor.run(-turn_speed)
            self.right_motor.run(turn_speed)
    
    def drive_straight(self, distance_mm, speed=50, decel_distance_mm=100):
        """
        Drive straight for a specified distance using encoders and gyro correction.
        
        Args:
            distance_mm: Distance to travel in millimeters
            speed: Base speed (numeric scale)
            decel_distance_mm: Distance before target to start decelerating
        """
        target_ticks = self.mm_to_ticks(distance_mm)
        target_heading = self.gyro.angle()
        
        # Reset encoders for this movement
        self.left_motor.reset_angle(0)
        self.right_motor.reset_angle(0)
        self.heading_pid.reset()
        
        while True:
            # Get current position (average of both encoders)
            left_ticks = self.left_motor.angle()
            right_ticks = self.right_motor.angle()
            avg_ticks = (left_ticks + right_ticks) / 2.0
            
            # Calculate distance error
            distance_error = target_ticks - avg_ticks
            
            # Check if reached target
            if abs(distance_error) < self.mm_to_ticks(5):  # 5mm tolerance
                self.left_motor.stop()
                self.right_motor.stop()
                break
            
            # Calculate base speed with simple deceleration
            remaining_distance_mm = abs(self.ticks_to_mm(distance_error))
            if remaining_distance_mm < decel_distance_mm:
                # Linear deceleration
                speed_scale = max(0.3, remaining_distance_mm / decel_distance_mm)
                current_speed = speed * speed_scale * sign(distance_error)
            else:
                current_speed = speed * sign(distance_error)
            
            # Gyro correction for straight driving
            heading_error = trimmed_angle_deg(target_heading - self.gyro.angle())
            correction = self.heading_pid.compute(heading_error)
            correction = clamp(correction, -20, 20)
            
            # Apply motor speeds with correction
            left_speed = current_speed - correction
            right_speed = current_speed + correction
            
            self.left_motor.run(left_speed)
            self.right_motor.run(right_speed)
