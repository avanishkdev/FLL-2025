"""Utility functions for robot control."""

import time


def clamp(value, min_value, max_value):
    """Clamp value between min_value and max_value."""
    return max(min_value, min(max_value, value))


def trimmed_angle_deg(angle):
    """Normalize angle to [-180, 180] range."""
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle


def sign(value):
    """Return the sign of a value (-1, 0, or 1)."""
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0


class Timer:
    """Simple timer for measuring elapsed time."""
    
    def __init__(self):
        self.start_time = None
    
    def start(self):
        """Start or restart the timer."""
        self.start_time = time.time()
    
    def elapsed_ms(self):
        """Return elapsed time in milliseconds."""
        if self.start_time is None:
            return 0
        return int((time.time() - self.start_time) * 1000)
    
    def elapsed_s(self):
        """Return elapsed time in seconds."""
        if self.start_time is None:
            return 0
        return time.time() - self.start_time
