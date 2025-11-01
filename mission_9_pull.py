"""
Mission 9 Pull - Shim to use refactored robot package.

This file provides backward compatibility with Menu.py by preserving
the original Missioon_9__Pull() function name and execution behavior,
while delegating to the new DriveController-based implementation.
"""

from robot.missions.pybricks_mission_9_pull import run_mission_9_pull


def Missioon_9__Pull():
    """
    Execute Mission 9 Pull using the refactored robot control package.
    
    This function is called by Menu.py and maintains the original name
    for compatibility.
    """
    run_mission_9_pull()


# The main program starts here - preserve original execution behavior
Missioon_9__Pull()
