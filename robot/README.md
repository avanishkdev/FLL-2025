# Robot Control Package

This package provides a centralized control system for the FLL 2025 robot with abstracted hardware interfaces and navigation primitives.

## Architecture

- **utils.py**: Utility functions (clamp, trimmed_angle_deg, Timer, sign)
- **pid.py**: PID controller with anti-windup and derivative filtering
- **motors.py**: Motor hardware abstraction (MotorHardware, MotorController)
- **navigation.py**: DriveController with gyro-based turn_to and drive_straight
- **pybricks_adapters.py**: Pybricks-specific hardware adapters

## Usage

### Basic Example

```python
from robot.pybricks_adapters import create_pybricks_hardware
from robot.motors import MotorController
from robot.navigation import DriveController

# Create hardware
hw = create_pybricks_hardware()

# Reset sensors
hw['gyro'].reset()
hw['left_motor'].reset_angle(0)
hw['right_motor'].reset_angle(0)

# Create motor controllers
left_controller = MotorController(hw['left_motor'])
right_controller = MotorController(hw['right_motor'])

# Create drive controller
drive = DriveController(
    left_motor=left_controller,
    right_motor=right_controller,
    gyro=hw['gyro'],
    wheel_diameter_mm=56,
    wheel_base_mm=80
)

# Drive straight 300mm at 50% speed
drive.drive_straight(300, base_speed=50)

# Turn to 90 degrees heading
drive.turn_to(90, max_speed=30)
```

## Hardware Configuration

Port mappings (from mission_9_pull.py):
- **Right motor**: Port.C, Direction.CLOCKWISE
- **Left motor**: Port.A, Direction.COUNTERCLOCKWISE (reversed in adapter)
- **Left gear**: Port.B (manipulator)

Robot parameters:
- **Wheel diameter**: 56mm
- **Wheel base**: 80mm
- **Encoder resolution**: 360 ticks per revolution

## Migration Notes

To migrate existing missions:

1. Import the robot package modules
2. Create hardware using `create_pybricks_hardware()`
3. Create motor controllers and drive controller
4. Replace DriveBase calls:
   - `drive_base.straight(distance)` → `drive.drive_straight(distance, base_speed=50)`
   - `drive_base.turn(angle)` → compute target heading and use `drive.turn_to(target)`
5. Keep manipulator calls (e.g., `left_gear.run_angle()`) unchanged

See `robot/missions/pybricks_mission_9_pull.py` for a complete example.

## Tuning

See TUNING.md in the repository root for PID tuning instructions and parameter adjustment guidelines.
