# Robot Control Package

This package provides reusable PID, motor, sensor, and navigation modules for Spike Prime / Pybricks robots.

## Overview

The robot package centralizes navigation primitives with gyro and encoder closed-loop control, improving predictability and reducing overshoot/undershoot compared to ad-hoc DriveBase calls.

## Modules

- **utils.py**: Helper functions (clamp, angle normalization, Timer)
- **pid.py**: PID controller with anti-windup and derivative filtering
- **motors.py**: MotorHardware interface and MotorController for encoder-based control
- **navigation.py**: DriveController implementing drive_straight and turn_to with heading-hold
- **pybricks_adapters.py**: Spike Prime hardware adapters (motors, gyro)

## Usage

### Basic Setup

```python
from robot.motors import MotorController
from robot.navigation import DriveController
from robot.pybricks_adapters import create_spike_prime_robot

# Create robot hardware with standard port mapping
robot = create_spike_prime_robot(
    wheel_diameter_mm=56,
    wheel_base_mm=80,
    ticks_per_rev=360
)

# Create motor controllers
left_controller = MotorController(robot['left_hw'])
right_controller = MotorController(robot['right_hw'])

# Create drive controller
drive = DriveController(
    left_motor=left_controller,
    right_motor=right_controller,
    gyro=robot['gyro'],
    wheel_diameter_mm=56,
    wheel_base_mm=80,
    ticks_per_rev=360
)

# Reset sensors before starting
drive.reset()
```

### Navigation Commands

```python
# Drive straight 500mm at 50% speed
drive.drive_straight(500, speed=50)

# Turn to absolute heading of 90 degrees
drive.turn_to(90, speed=40)

# Turn relative to current heading (45 degrees right)
drive.turn_relative(45, speed=40)

# Drive backward 200mm
drive.drive_straight(-200, speed=50)
```

### Manipulator Control

The left_gear motor (Port B) is available for manipulator actions:

```python
# Access manipulator motor
robot['left_gear'].run_angle(1000, 650)
```

## Hardware Configuration

Default port mapping (from mission_9_pull.py):
- **Left motor**: Port.A with Direction.COUNTERCLOCKWISE
- **Right motor**: Port.C with Direction.CLOCKWISE  
- **Left gear (manipulator)**: Port.B with Direction.CLOCKWISE

## Migrating Existing Missions

To migrate a mission file to use the new robot package:

1. Import the robot modules at the top of your mission file
2. Replace DriveBase setup with DriveController setup
3. Replace `drive_base.straight(distance)` calls with `drive.drive_straight(distance, speed=50)`
4. Replace `drive_base.turn(angle)` calls with `drive.turn_relative(angle, speed=40)`
5. Keep manipulator motor calls unchanged

### Example Migration

**Before:**
```python
drive_base.straight(180)
drive_base.turn(-85)
```

**After:**
```python
drive.drive_straight(180, speed=50)
drive.turn_relative(-85, speed=40)
```

## Tuning

For PID tuning and parameter adjustment, see [TUNING.md](../TUNING.md) in the repository root.

## Testing

Test the robot setup with a simple sequence:

```python
# Reset and test forward/backward
drive.reset()
drive.drive_straight(100, speed=30)
drive.drive_straight(-100, speed=30)

# Test turning
drive.turn_relative(90, speed=30)
drive.turn_relative(-90, speed=30)
```

Adjust PID gains in `navigation.py` if the robot overshoots or oscillates.
