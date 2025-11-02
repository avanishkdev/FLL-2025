"""Utility functions for robot control."""

import time


def clamp(value, min_value, max_value):
    """Clamp a value between min and max bounds."""
    return max(min_value, min(max_value, value))


def trimmed_angle_deg(angle):
    """Normalize angle to [-180, 180] range."""
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle


def sign(value):
    """Return the sign of a value: -1, 0, or 1."""
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0


class Timer:
    """Simple timer for tracking elapsed time."""
    
    def __init__(self):
        """Initialize timer."""
        self._start_time = None
    
    def reset(self):
        """Reset the timer to current time."""
        self._start_time = time.time()
    
    def time(self):
        """Get elapsed time in milliseconds since reset."""
        if self._start_time is None:
            return 0
        return int((time.time() - self._start_time) * 1000)
