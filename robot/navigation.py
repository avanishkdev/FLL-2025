"""
Navigation controller for differential drive robots with gyro feedback.
"""

from robot.pid import PIDController
from robot.utils import normalize_angle, clamp, Timer


class GyroAdapter:
    """Abstract interface for gyro sensor."""
    
    def get_angle(self):
        """Get current heading in degrees."""
        raise NotImplementedError
    
    def reset(self):
        """Reset gyro to zero."""
        raise NotImplementedError


class DriveController:
    """
    Drive controller that uses motor controllers and gyro for closed-loop navigation.
    Implements drive_straight with heading hold and turn_to with gyro feedback.
    """
    
    def __init__(self, left_motor, right_motor, gyro, wheel_diameter_mm=56, wheel_base_mm=80, ticks_per_rev=360):
        """
        Initialize drive controller.
        
        Args:
            left_motor: MotorController for left motor
            right_motor: MotorController for right motor
            gyro: GyroAdapter instance
            wheel_diameter_mm: Wheel diameter in millimeters
            wheel_base_mm: Distance between wheels in millimeters
            ticks_per_rev: Encoder ticks per wheel revolution
        """
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.gyro = gyro
        self.wheel_diameter_mm = wheel_diameter_mm
        self.wheel_base_mm = wheel_base_mm
        self.ticks_per_rev = ticks_per_rev
        
        # PID controllers for heading hold and turning
        self.heading_pid = PIDController(kp=1.5, ki=0.0, kd=0.3, output_min=-30, output_max=30)
        self.turn_pid = PIDController(kp=1.2, ki=0.0, kd=0.2, output_min=-50, output_max=50)
        
        self.timer = Timer()
    
    def reset(self):
        """Reset encoders and gyro."""
        self.left_motor.reset_encoder()
        self.right_motor.reset_encoder()
        self.gyro.reset()
        self.heading_pid.reset()
        self.turn_pid.reset()
    
    def drive_straight(self, distance_mm, speed=50, timeout_ms=10000):
        """
        Drive straight for a specified distance with heading hold.
        
        Args:
            distance_mm: Distance to travel in millimeters
            speed: Base speed (0-100)
            timeout_ms: Maximum time to wait in milliseconds
        
        Returns:
            True if completed successfully, False if timeout
        """
        # Calculate target encoder ticks
        wheel_circumference = 3.14159 * self.wheel_diameter_mm
        target_ticks = (distance_mm / wheel_circumference) * self.ticks_per_rev
        
        # Reset and start
        initial_left = self.left_motor.hw.get_angle()
        initial_right = self.right_motor.hw.get_angle()
        target_heading = self.gyro.get_angle()
        
        self.heading_pid.reset()
        self.timer.reset()
        
        tolerance = 20  # ticks
        
        while self.timer.time() < timeout_ms:
            # Calculate distance traveled
            left_ticks = self.left_motor.hw.get_angle() - initial_left
            right_ticks = self.right_motor.hw.get_angle() - initial_right
            avg_ticks = (left_ticks + right_ticks) / 2.0
            
            distance_error = target_ticks - avg_ticks
            
            # Check if we've reached the target
            if abs(distance_error) < tolerance:
                self.left_motor.hw.stop()
                self.right_motor.hw.stop()
                return True
            
            # Heading correction
            current_heading = self.gyro.get_angle()
            heading_error = normalize_angle(target_heading - current_heading)
            correction = self.heading_pid.update(heading_error)
            
            # Calculate motor powers with deceleration near target
            if abs(distance_error) < abs(target_ticks) * 0.3:
                # Decelerate in final 30%
                current_speed = speed * (abs(distance_error) / (abs(target_ticks) * 0.3))
                current_speed = max(20, min(speed, current_speed))
            else:
                current_speed = speed
            
            # Apply direction based on target distance
            if distance_mm < 0:
                current_speed = -current_speed
            
            left_power = clamp(current_speed + correction, -100, 100)
            right_power = clamp(current_speed - correction, -100, 100)
            
            self.left_motor.hw.set_power(left_power)
            self.right_motor.hw.set_power(right_power)
        
        # Timeout
        self.left_motor.hw.stop()
        self.right_motor.hw.stop()
        return False
    
    def turn_to(self, target_angle, speed=40, timeout_ms=5000):
        """
        Turn to an absolute heading using gyro feedback.
        
        Args:
            target_angle: Target heading in degrees
            speed: Maximum turn speed (0-100)
            timeout_ms: Maximum time to wait in milliseconds
        
        Returns:
            True if completed successfully, False if timeout
        """
        self.turn_pid.reset()
        self.timer.reset()
        
        tolerance = 2  # degrees
        
        while self.timer.time() < timeout_ms:
            current_angle = self.gyro.get_angle()
            error = normalize_angle(target_angle - current_angle)
            
            # Check if we've reached the target
            if abs(error) < tolerance:
                self.left_motor.hw.stop()
                self.right_motor.hw.stop()
                return True
            
            # Calculate turn power with PID
            turn_power = self.turn_pid.update(error)
            
            # Apply deceleration near target
            if abs(error) < 20:
                scale = abs(error) / 20.0
                turn_power = turn_power * scale
            
            # Scale to speed limit
            if abs(turn_power) > speed:
                turn_power = speed if turn_power > 0 else -speed
            
            # Set motor powers (positive = turn right)
            self.left_motor.hw.set_power(turn_power)
            self.right_motor.hw.set_power(-turn_power)
        
        # Timeout
        self.left_motor.hw.stop()
        self.right_motor.hw.stop()
        return False
    
    def turn_relative(self, angle_deg, speed=40, timeout_ms=5000):
        """
        Turn relative to current heading.
        
        Args:
            angle_deg: Relative angle to turn (positive = right)
            speed: Maximum turn speed (0-100)
            timeout_ms: Maximum time to wait in milliseconds
        
        Returns:
            True if completed successfully, False if timeout
        """
        current = self.gyro.get_angle()
        target = normalize_angle(current + angle_deg)
        return self.turn_to(target, speed, timeout_ms)
