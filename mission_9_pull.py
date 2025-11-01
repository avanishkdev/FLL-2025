"""
Mission 9 Pull - Shim for backward compatibility with Menu.py

This file has been refactored to use the centralized robot control package.
The original mission logic is now in robot/missions/pybricks_mission_9_pull.py
"""

from robot.missions.pybricks_mission_9_pull import run_mission_9_pull


def Missioon_9__Pull():
    """Execute Mission 9 Pull using the refactored robot control package."""
    run_mission_9_pull()


# The main program starts here (called by Menu.py when this module is imported)
Missioon_9__Pull()
