# Robot Tuning Guide

This document provides tuning instructions for the robot control system.

## Quick Reference

### Motor Speed Mapping

- `MAX_DEG_PER_SEC = 1080`: Maximum motor speed in degrees/second
- Speed percentage (-100 to 100) maps to motor.run(deg_s) via: `deg_s = (speed_percent / 100) * 1080`
- Example: 50% speed = 540 deg/s

### Robot Physical Constants

Located in `robot/pybricks_adapters.py` and `DriveController`:

```python
wheel_diameter_mm = 56    # Wheel diameter
wheel_base_mm = 80        # Distance between wheels
ticks_per_rev = 360       # Encoder ticks per revolution
wheel_circumference = π * 56 mm  # ≈ 175.93 mm
```

### Port and Direction Mappings

From mission_9_pull.py configuration:

- **Right motor**: Port.C, Direction.CLOCKWISE (`positive_direction=1`)
- **Left motor**: Port.A, Direction.COUNTERCLOCKWISE (`positive_direction=-1`)
- **Left gear**: Port.B (manipulator)

The left motor direction is reversed in the adapter because the original used COUNTERCLOCKWISE.

## PID Tuning

### Heading PID (for straight driving and turning)

Default values in `DriveController.__init__()`:

```python
heading_kp = 2.0   # Proportional gain
heading_ki = 0.1   # Integral gain
heading_kd = 0.5   # Derivative gain
```

#### Tuning Process

1. **Test on robot**: Run small test movements
   ```python
   drive.turn_to(45, max_speed=20)  # Small turn
   drive.drive_straight(200, base_speed=30)  # Short drive
   ```

2. **Tune P term first**:
   - If robot oscillates: reduce `heading_kp`
   - If robot turns too slowly: increase `heading_kp`
   - Start with `heading_kp=1.0` and adjust by 0.5 increments

3. **Add D term**:
   - Reduces overshoot and oscillation
   - Start with `heading_kd=0.5`
   - Increase if robot still oscillates

4. **Add I term last**:
   - Eliminates steady-state error
   - Keep small (0.05 to 0.2)
   - Too high causes instability

5. **Update in code**: Modify `DriveController` initialization in mission files or create a tuning configuration file.

### Speed Tuning

In `robot/missions/pybricks_mission_9_pull.py`:

```python
drive_speed = 50  # Base speed for driving (0-100)
turn_speed = 30   # Base speed for turning (0-100)
```

- **Too slow**: Increase values by 10
- **Too fast/aggressive**: Decrease values by 10
- **Motors stalling**: Check if MAX_DEG_PER_SEC is too high

### Deceleration Tuning

In `DriveController.drive_straight()`:

```python
if remaining_mm < 100:
    speed_multiplier = max(0.3, remaining_mm / 100)
```

- **Overshoots target**: Increase deceleration distance (e.g., 150mm) or reduce minimum speed (e.g., 0.2)
- **Stops too early**: Decrease deceleration distance (e.g., 75mm) or increase minimum speed (e.g., 0.4)

## Testing Procedure

### 1. Verify Gyro

```python
hw = create_pybricks_hardware()
print(hw['gyro'].get_angle())  # Should read ~0 after reset
hw['gyro'].reset()
# Manually turn robot, verify reading changes
```

### 2. Test Turn

```python
drive.turn_to(90, max_speed=20)
# Verify robot turns approximately 90 degrees
# Check for oscillation or overshoot
```

### 3. Test Straight Drive

```python
drive.drive_straight(300, base_speed=30)
# Verify robot drives approximately 300mm
# Mark start position and measure
```

### 4. Run Full Mission

```python
from robot.missions.pybricks_mission_9_pull import run_mission_9_pull
run_mission_9_pull()
# Verify complete sequence works as expected
```

## Troubleshooting

### Robot Doesn't Move

- Check motor connections (Ports A, B, C)
- Verify MAX_DEG_PER_SEC isn't set too low
- Check battery level

### Robot Drifts During Straight Drive

- Increase `heading_kp` (proportional gain)
- Verify gyro is working: `hw['gyro'].get_angle()`
- Check wheel diameters are equal and accurate

### Robot Oscillates During Turn

- Decrease `heading_kp`
- Increase `heading_kd`
- Reduce `max_speed` parameter in `turn_to()`

### Robot Overshoots Target

- Reduce base_speed
- Increase deceleration distance
- Add delay after movements

### Motors Are Too Aggressive

- Reduce MAX_DEG_PER_SEC (try 720 or 540)
- Reduce base_speed and turn_speed in missions
- Check that speed percentages aren't too high

## Configuration Files

To avoid modifying code for tuning, consider creating a configuration file:

```python
# config.py
TUNING = {
    'heading_kp': 2.0,
    'heading_ki': 0.1,
    'heading_kd': 0.5,
    'drive_speed': 50,
    'turn_speed': 30,
    'max_deg_per_sec': 1080
}
```

Then import and use in missions:

```python
from config import TUNING
drive = DriveController(..., heading_kp=TUNING['heading_kp'], ...)
```
