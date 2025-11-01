# Robot Control Package

This package provides a centralized, reusable robot control framework for FLL missions.

## Structure

```
robot/
├── utils.py              # Utility functions (clamp, angle normalization, Timer)
├── pid.py                # PID controller with anti-windup
├── motors.py             # MotorController for encoder-based control
├── navigation.py         # DriveController for precise movement
├── pybricks_adapters.py  # Pybricks hardware configuration
└── missions/             # Refactored missions
    └── pybricks_mission_9_pull.py
```

## Key Components

### MotorController
Wraps Pybricks Motor with:
- Numeric speed scale (-100 to 100)
- Direction normalization
- Encoder-based distance control
- Access to hardware via `.hw` attribute

### DriveController
Provides high-level navigation primitives:
- `drive_straight(distance_mm, speed)` - Straight driving with gyro correction and deceleration
- `turn_to(angle, speed)` - Absolute heading turns using gyro
- Automatic PID-based heading correction

### PID Controller
Full-featured PID implementation with:
- Anti-windup protection
- Optional derivative filtering
- Configurable gains and limits

## Usage Example

```python
from robot.pybricks_adapters import create_robot_from_mission_9_config

# Create robot
robot = create_robot_from_mission_9_config()
drive = robot['drive_controller']

# Initialize
drive.reset()

# Drive 500mm forward
drive.drive_straight(500, speed=50)

# Turn to 90 degrees
drive.turn_to(90, speed=40)
```

## Migration Guide

When migrating existing missions:

1. **Import the adapter**: `from robot.pybricks_adapters import create_robot_from_mission_9_config`
2. **Create robot**: `robot = create_robot_from_mission_9_config()`
3. **Replace DriveBase calls**:
   - `drive_base.straight(distance)` → `drive.drive_straight(distance, speed)`
   - `drive_base.turn(angle)` → update heading and call `drive.turn_to(new_heading, speed)`
4. **Replace motor calls**: Access hardware via `robot['left_gear']` directly
5. **Initialize**: Call `drive.reset()` at mission start

## Configuration

Default parameters (from mission_9_pull.py):
- Wheel diameter: 56mm
- Wheel base: 80mm
- Ticks per revolution: 360
- Max motor speed: 1080 deg/s
- Left motor: Port.A, COUNTERCLOCKWISE (positive_direction=-1)
- Right motor: Port.C, CLOCKWISE (positive_direction=1)
- Manipulator: Port.B

## Testing

See TUNING.md for testing procedures and parameter tuning guidance.

## Notes

- All distances are in millimeters
- All angles are in degrees
- Speed scale is -100 to 100 (mapped to motor deg/s internally)
- Gyro heading is cumulative (not wrapped to 0-360)
