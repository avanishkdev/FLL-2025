"""Robot navigation with gyro and encoder-based control."""

import time
import math
from robot.pid import PID
from robot.utils import trimmed_angle_deg, clamp


class GyroAdapter:
    """Abstract interface for gyro hardware."""
    
    def get_heading(self):
        """Get current heading in degrees."""
        raise NotImplementedError
    
    def reset_heading(self, angle=0):
        """Reset heading to specified angle."""
        raise NotImplementedError


class DriveController:
    """Robot drive controller with gyro and encoder-based navigation."""
    
    def __init__(self, left_motor, right_motor, gyro, 
                 wheel_diameter_mm=56, wheel_base_mm=80):
        """
        Initialize drive controller.
        
        Args:
            left_motor: MotorController for left wheel
            right_motor: MotorController for right wheel
            gyro: GyroAdapter for heading
            wheel_diameter_mm: Wheel diameter in mm
            wheel_base_mm: Distance between wheels in mm
        """
        self.left = left_motor
        self.right = right_motor
        self.gyro = gyro
        self.wheel_diameter_mm = wheel_diameter_mm
        self.wheel_base_mm = wheel_base_mm
        
        # Calculate conversion factors
        self.wheel_circumference = math.pi * wheel_diameter_mm
        
        # PID controllers for heading and drive
        self.heading_pid = PID(kp=1.5, ki=0.01, kd=0.1, 
                              output_min=-30, output_max=30)
        self.drive_pid = PID(kp=0.5, ki=0.0, kd=0.0,
                            output_min=-20, output_max=20)
    
    def reset(self):
        """Reset encoders and gyro."""
        self.left.reset_angle(0)
        self.right.reset_angle(0)
        self.gyro.reset_heading(0)
    
    def turn_to(self, target_heading, timeout_ms=5000):
        """
        Turn to absolute heading using gyro.
        
        Args:
            target_heading: Target heading in degrees
            timeout_ms: Timeout in milliseconds
        
        Returns:
            True if target reached, False if timed out
        """
        self.heading_pid.reset()
        start_time = time.time()
        
        base_speed = 30  # Base turning speed
        tolerance = 2  # Heading tolerance in degrees
        settled_count = 0
        
        while True:
            # Check timeout
            elapsed_ms = (time.time() - start_time) * 1000
            if elapsed_ms > timeout_ms:
                self.left.stop()
                self.right.stop()
                return False
            
            # Get current heading and calculate error
            current_heading = self.gyro.get_heading()
            error = trimmed_angle_deg(target_heading - current_heading)
            
            # Check if we're at target
            if abs(error) < tolerance:
                settled_count += 1
                if settled_count >= 5:  # Settled for 5 iterations
                    self.left.hold()
                    self.right.hold()
                    return True
            else:
                settled_count = 0
            
            # Calculate control output
            correction = self.heading_pid.update(error)
            
            # Apply turn (positive error = turn right)
            turn_speed = base_speed if abs(error) > 10 else base_speed * 0.5
            left_speed = clamp(turn_speed + correction, -100, 100)
            right_speed = clamp(-turn_speed + correction, -100, 100)
            
            self.left.run(left_speed)
            self.right.run(right_speed)
            
            time.sleep(0.02)  # 50Hz update rate
    
    def drive_straight(self, distance_mm, base_speed=50, timeout_ms=10000):
        """
        Drive straight for specified distance using gyro and encoders.
        
        Args:
            distance_mm: Target distance in mm (positive = forward)
            base_speed: Base speed -100 to 100
            timeout_ms: Timeout in milliseconds
        
        Returns:
            True if target reached, False if timed out
        """
        # Convert distance to encoder degrees
        distance_deg = (distance_mm / self.wheel_circumference) * 360
        
        # Record starting position and heading
        start_left = self.left.get_angle()
        start_right = self.right.get_angle()
        target_heading = self.gyro.get_heading()
        
        self.heading_pid.reset()
        self.drive_pid.reset()
        start_time = time.time()
        
        tolerance = 20  # Position tolerance in degrees
        
        # Determine direction
        direction = 1 if distance_mm > 0 else -1
        abs_base_speed = abs(base_speed)
        
        while True:
            # Check timeout
            elapsed_ms = (time.time() - start_time) * 1000
            if elapsed_ms > timeout_ms:
                self.left.stop()
                self.right.stop()
                return False
            
            # Get current position
            current_left = self.left.get_angle()
            current_right = self.right.get_angle()
            avg_distance = ((current_left - start_left) + (current_right - start_right)) / 2
            
            # Check if we've reached target
            remaining = distance_deg - avg_distance
            if abs(remaining) < tolerance:
                self.left.hold()
                self.right.hold()
                return True
            
            # Simple deceleration
            if abs(remaining) < abs(distance_deg) * 0.2:  # Last 20% of distance
                current_speed = abs_base_speed * 0.5
            else:
                current_speed = abs_base_speed
            
            # Heading correction
            current_heading = self.gyro.get_heading()
            heading_error = trimmed_angle_deg(target_heading - current_heading)
            correction = self.heading_pid.update(heading_error)
            
            # Apply speeds with heading correction
            left_speed = direction * clamp(current_speed - correction, -100, 100)
            right_speed = direction * clamp(current_speed + correction, -100, 100)
            
            self.left.run(left_speed)
            self.right.run(right_speed)
            
            time.sleep(0.02)  # 50Hz update rate
