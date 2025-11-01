"""
Utility functions for robot control.
"""

from pybricks.tools import StopWatch


def clamp(value, min_value, max_value):
    """Clamp a value between min and max."""
    return max(min_value, min(max_value, value))


def normalize_angle(angle):
    """Normalize angle to [-180, 180] range."""
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle


class Timer:
    """Simple timer wrapper around StopWatch."""
    
    def __init__(self):
        self.stopwatch = StopWatch()
    
    def reset(self):
        """Reset the timer."""
        self.stopwatch.reset()
    
    def time(self):
        """Get elapsed time in milliseconds."""
        return self.stopwatch.time()
