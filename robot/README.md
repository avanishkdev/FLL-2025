# Robot Control Package

This package provides a centralized robot control framework with PID-based navigation, motor control, and Pybricks hardware adapters.

## Structure

- **utils.py** - Utility functions (clamp, angle normalization, timer, sign)
- **pid.py** - PID controller with anti-windup and derivative filtering
- **motors.py** - Motor hardware interface and controller with encoder-based movement
- **navigation.py** - DriveController with gyro and encoder-based navigation
- **pybricks_adapters.py** - Pybricks hardware adapters for motors and gyro
- **missions/** - Refactored mission files using the control framework

## Usage

### Basic Setup

```python
from robot.pybricks_adapters import create_robot_from_mission_9_config
from robot.navigation import DriveController

# Create hardware
left_motor, right_motor, gyro, manipulator = create_robot_from_mission_9_config()

# Create drive controller
drive = DriveController(left_motor, right_motor, gyro, 
                       wheel_diameter_mm=56, wheel_base_mm=80)

# Reset sensors
drive.reset()
```

### Navigation

```python
# Drive straight 300mm at 50% speed
drive.drive_straight(300, base_speed=50)

# Turn to absolute heading 90 degrees
drive.turn_to(90)

# Turn relative to current heading
current = gyro.get_heading()
drive.turn_to(current + 45)  # Turn right 45 degrees
```

### Motor Control

```python
# Run motor at speed
motor.run(50)  # 50% speed

# Drive to distance
motor.drive_to_distance(360, speed=50)  # 360 degrees

# Use manipulator (direct Pybricks Motor)
manipulator.run_angle(1000, 650)  # Run at 1000 deg/s for 650 degrees
```

## Migration Notes

### Converting Existing Missions

Original mission code using DriveBase:
```python
drive_base.straight(180)
drive_base.turn(-85)
```

Refactored using DriveController:
```python
drive.drive_straight(180, base_speed=50)
current = gyro.get_heading()
drive.turn_to(current - 85)
```

### Key Differences

1. **Turns are absolute** - Use `turn_to(heading)` instead of `turn(angle)`
2. **Speeds are normalized** - Range -100 to 100 (internally mapped to deg/s)
3. **Gyro-based** - Better accuracy for straight driving and turning
4. **Timeout protection** - All movements have configurable timeouts

### Hardware Configuration

The default configuration matches `mission_9_pull.py`:
- Right motor: Port C, Direction.CLOCKWISE
- Left motor: Port A, Direction.COUNTERCLOCKWISE
- Manipulator: Port B, Direction.CLOCKWISE
- Wheel diameter: 56mm
- Wheel base: 80mm
- Encoder resolution: 360 ticks/rev

## Tuning

See `TUNING.md` in the repository root for detailed tuning instructions.
