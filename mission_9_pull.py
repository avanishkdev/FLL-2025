"""
Mission 9 Pull - Shim for backward compatibility with Menu.py

This file imports the refactored mission from the robot package
and provides the same Missioon_9__Pull() function interface.
"""

from robot.missions.pybricks_mission_9_pull import run_mission_9_pull


def Missioon_9__Pull():
    """Execute Mission 9 Pull using the refactored robot control framework."""
    run_mission_9_pull()


# The main program starts here (called when imported by Menu.py)
Missioon_9__Pull()
