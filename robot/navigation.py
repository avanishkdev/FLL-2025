"""Navigation controller with gyro and encoder feedback."""

import math
from robot.pid import PID
from robot.utils import clamp, trimmed_angle_deg, Timer, sign


class DriveController:
    """Drive controller with turn_to and drive_straight using gyro + encoders."""
    
    def __init__(self, left_motor, right_motor, gyro, wheel_diameter_mm=56, 
                 wheel_base_mm=80, heading_kp=2.0, heading_ki=0.1, heading_kd=0.5):
        """
        Initialize drive controller.
        
        Args:
            left_motor: MotorController instance for left motor
            right_motor: MotorController instance for right motor
            gyro: Gyro adapter with get_angle() method
            wheel_diameter_mm: Wheel diameter in mm
            wheel_base_mm: Distance between wheels in mm
            heading_kp: Heading PID proportional gain
            heading_ki: Heading PID integral gain
            heading_kd: Heading PID derivative gain
        """
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.gyro = gyro
        self.wheel_diameter_mm = wheel_diameter_mm
        self.wheel_base_mm = wheel_base_mm
        
        # PID controller for heading
        self.heading_pid = PID(heading_kp, heading_ki, heading_kd, output_limit=50)
        
        # Wheel circumference
        self.wheel_circumference_mm = math.pi * wheel_diameter_mm
    
    def turn_to(self, target_heading, max_speed=30, timeout_ms=5000):
        """
        Turn to target heading using gyro feedback.
        
        Args:
            target_heading: Target heading in degrees
            max_speed: Maximum turn speed percentage
            timeout_ms: Timeout in milliseconds
            
        Returns:
            True if reached target, False if timed out
        """
        self.heading_pid.reset()
        timer = Timer()
        
        while timer.time() < timeout_ms:
            current_heading = self.gyro.get_angle()
            error = trimmed_angle_deg(target_heading - current_heading)
            
            # Check if we're close enough
            if abs(error) < 2:  # 2 degree threshold
                break
            
            # Calculate turn speed from PID
            turn_speed = self.heading_pid.update(error)
            turn_speed = clamp(turn_speed, -max_speed, max_speed)
            
            # Apply differential drive (turn in place)
            self.left_motor.hw.set_speed(-turn_speed * 10.8)  # Convert to deg/sec
            self.right_motor.hw.set_speed(turn_speed * 10.8)
        
        # Stop motors
        self.left_motor.hw.stop()
        self.right_motor.hw.stop()
        
        # Check if we reached target
        final_heading = self.gyro.get_angle()
        return abs(trimmed_angle_deg(target_heading - final_heading)) < 5
    
    def drive_straight(self, distance_mm, base_speed=50, timeout_ms=10000):
        """
        Drive straight for specified distance using gyro and encoders.
        
        Args:
            distance_mm: Distance to travel in mm (positive=forward, negative=backward)
            base_speed: Base speed percentage
            timeout_ms: Timeout in milliseconds
            
        Returns:
            True if reached target, False if timed out
        """
        # Record target heading
        target_heading = self.gyro.get_angle()
        
        # Reset PID
        self.heading_pid.reset()
        
        # Calculate distance in degrees
        distance_deg = (distance_mm / self.wheel_circumference_mm) * 360
        
        # Record start positions
        start_left = self.left_motor.hw.get_angle()
        start_right = self.right_motor.hw.get_angle()
        target_left = start_left + distance_deg
        target_right = start_right + distance_deg
        
        # Determine direction
        direction = sign(distance_mm)
        if direction == 0:
            return True
        
        timer = Timer()
        
        while timer.time() < timeout_ms:
            # Get current positions
            current_left = self.left_motor.hw.get_angle()
            current_right = self.right_motor.hw.get_angle()
            
            # Calculate remaining distance (average of both wheels)
            remaining_left = abs(target_left - current_left)
            remaining_right = abs(target_right - current_right)
            remaining = (remaining_left + remaining_right) / 2
            
            # Check if we're close enough
            if remaining < 10:  # 10 degree threshold
                break
            
            # Simple deceleration: reduce speed in last 100mm
            remaining_mm = (remaining / 360) * self.wheel_circumference_mm
            speed_multiplier = 1.0
            if remaining_mm < 100:
                speed_multiplier = max(0.3, remaining_mm / 100)
            
            current_speed = base_speed * speed_multiplier
            
            # Get heading correction from PID
            current_heading = self.gyro.get_angle()
            heading_error = trimmed_angle_deg(target_heading - current_heading)
            correction = self.heading_pid.update(heading_error) * 0.5  # Reduce correction strength
            
            # Apply speeds with correction
            left_speed = (current_speed + correction) * direction
            right_speed = (current_speed - correction) * direction
            
            # Clamp speeds
            left_speed = clamp(left_speed, -100, 100)
            right_speed = clamp(right_speed, -100, 100)
            
            # Convert to deg/sec and apply
            self.left_motor.hw.set_speed(left_speed * 10.8)
            self.right_motor.hw.set_speed(right_speed * 10.8)
        
        # Stop motors
        self.left_motor.hw.stop()
        self.right_motor.hw.stop()
        
        # Check if we reached target
        final_left = self.left_motor.hw.get_angle()
        final_right = self.right_motor.hw.get_angle()
        distance_traveled = ((final_left - start_left) + (final_right - start_right)) / 2
        return abs(distance_deg - distance_traveled) < 50
