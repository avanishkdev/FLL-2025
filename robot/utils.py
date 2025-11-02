"""Utility functions for robot control."""

from pybricks.tools import StopWatch


def clamp(value, min_value, max_value):
    """Clamp value between min and max."""
    return max(min_value, min(max_value, value))


def trimmed_angle_deg(angle):
    """Normalize angle to -180..180 degree range."""
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle


def sign(value):
    """Return sign of value (-1, 0, or 1)."""
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0


class Timer:
    """Simple timer wrapper around StopWatch."""
    
    def __init__(self):
        self.stopwatch = StopWatch()
        self.stopwatch.reset()
    
    def reset(self):
        """Reset the timer."""
        self.stopwatch.reset()
    
    def time(self):
        """Get elapsed time in milliseconds."""
        return self.stopwatch.time()
