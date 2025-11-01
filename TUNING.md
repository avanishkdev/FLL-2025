# Robot Control Tuning Guide

This guide provides instructions for tuning PID gains and mapping constants for optimal robot performance.

## Overview

The robot control package uses PID controllers for:
- **Heading hold** during straight-line driving (keeps robot going straight)
- **Turn control** for accurate angle targeting

## Quick Start Testing

Before tuning, verify basic operation:

1. **Test Gyro Orientation**:
   ```python
   from robot.pybricks_adapters import create_spike_prime_robot
   
   robot = create_spike_prime_robot()
   robot['gyro'].reset()
   print(robot['gyro'].get_angle())  # Should be ~0
   
   # Manually turn robot 90 degrees clockwise
   print(robot['gyro'].get_angle())  # Should be ~90
   ```

2. **Test Encoder Direction**:
   ```python
   # Reset encoders
   robot['left_hw'].reset_angle(0)
   robot['right_hw'].reset_angle(0)
   
   # Set motors to move forward
   robot['left_hw'].set_power(30)
   robot['right_hw'].set_power(30)
   
   # After 1 second, check encoders (should be positive for forward)
   print(robot['left_hw'].get_angle())
   print(robot['right_hw'].get_angle())
   ```

## PID Tuning

### Heading Hold PID (for drive_straight)

Located in `robot/navigation.py`, line ~51:
```python
self.heading_pid = PIDController(kp=1.5, ki=0.0, kd=0.3, output_min=-30, output_max=30)
```

**Tuning procedure:**
1. Start with `kp=1.0, ki=0.0, kd=0.0`
2. Increase `kp` until robot corrects heading drift quickly but doesn't oscillate
3. Add `kd` (start with `kd = kp/5`) to reduce oscillation
4. Only add `ki` if robot has persistent steady-state error (usually not needed)

**Symptoms:**
- **Robot drifts**: Increase `kp`
- **Robot oscillates/zigzags**: Decrease `kp`, increase `kd`
- **Sluggish correction**: Increase `kp` or decrease `kd`

### Turn PID (for turn_to)

Located in `robot/navigation.py`, line ~52:
```python
self.turn_pid = PIDController(kp=1.2, ki=0.0, kd=0.2, output_min=-50, output_max=50)
```

**Tuning procedure:**
1. Start with `kp=1.0, ki=0.0, kd=0.0`
2. Test with `drive.turn_relative(90, speed=40)`
3. Increase `kp` until turn is responsive but doesn't overshoot much
4. Add `kd` to dampen overshoot
5. Adjust `output_max` to limit maximum turn speed (current: 50)

**Symptoms:**
- **Undershoots target angle**: Increase `kp`
- **Overshoots and oscillates**: Decrease `kp`, increase `kd`
- **Too slow**: Increase `kp` or `output_max`

## Speed Mapping

### Motor Power to Speed

In `robot/pybricks_adapters.py`, the MAX_DEG_PER_SEC constant maps power values:
```python
MAX_DEG_PER_SEC = 1080  # Maximum motor speed in degrees/second
```

**Adjustment:**
- Decrease to limit maximum robot speed (e.g., 720 for slower, more controlled motion)
- Increase for faster motion (max ~1500, but may reduce precision)

### Speed Parameters

In mission files (e.g., `robot/missions/pybricks_mission_9_pull.py`):
```python
base_speed = 50  # 0-100 scale
turn_speed = 40  # 0-100 scale
```

**Recommendations:**
- **base_speed**: 30-60 for missions (50 = ~540 deg/s with default MAX_DEG_PER_SEC)
- **turn_speed**: 30-50 for turns (40 = ~430 deg/s)
- Lower speeds = more accurate, slower missions
- Higher speeds = faster but may reduce precision

## Wheel and Encoder Constants

In `robot/pybricks_adapters.py` and mission files:
```python
wheel_diameter_mm = 56   # Measure actual wheel diameter
wheel_base_mm = 80       # Measure distance between wheel centers
ticks_per_rev = 360      # Pybricks motor default
```

**Calibration:**
1. **wheel_diameter_mm**: Measure wheel diameter with calipers
2. **wheel_base_mm**: Measure center-to-center distance between drive wheels
3. **ticks_per_rev**: Keep at 360 for Pybricks motors

If `drive_straight(1000)` doesn't travel exactly 1000mm:
- **Travels too far**: Decrease `wheel_diameter_mm`
- **Travels too short**: Increase `wheel_diameter_mm`

If turns are not accurate:
- **Turns too much**: Decrease `wheel_base_mm`
- **Turns too little**: Increase `wheel_base_mm`

## Deceleration Tuning

The `drive_straight` method decelerates in the final 30% of distance. Adjust in `robot/navigation.py`:
```python
if abs(distance_error) < abs(target_ticks) * 0.3:  # Deceleration zone
    current_speed = speed * (abs(distance_error) / (abs(target_ticks) * 0.3))
    current_speed = max(20, min(speed, current_speed))  # Minimum speed
```

**Adjustments:**
- Change `0.3` to `0.5` for earlier/gentler deceleration
- Change `max(20, ...)` to adjust minimum speed during deceleration

## Timeout Values

Default timeouts in `robot/navigation.py`:
- `drive_straight`: 10000ms (10 seconds)
- `turn_to`: 5000ms (5 seconds)

Increase if robot needs more time for long distances or slow speeds.

## Troubleshooting

### Robot doesn't move
- Check motor directions in `pybricks_adapters.py`
- Verify `set_power` is being called with non-zero values
- Check battery level

### Robot turns opposite direction
- Swap left/right motor assignments in `create_spike_prime_robot()`
- Or adjust motor Direction parameters

### Encoders count wrong direction
- Verify motor Direction settings match physical wiring
- Check that positive power results in forward motion

### Gyro drift over time
- This is normal; reset gyro between runs with `drive.reset()`
- Keep robot stationary during gyro reset

## Testing Checklist

Before running missions on the competition field:

- [ ] Test drive_straight(100) and verify distance
- [ ] Test turn_relative(90) four times, verify robot returns to start heading
- [ ] Test backward drive with drive_straight(-100)
- [ ] Run a simple test mission with multiple straight/turn sequences
- [ ] Verify manipulator motor (left_gear) operates correctly
- [ ] Check that gyro.reset() properly resets heading to 0

## Advanced: Custom PID per Mission

If different missions need different PID gains, modify the DriveController after creation:
```python
drive.heading_pid.kp = 2.0
drive.heading_pid.kd = 0.5
drive.turn_pid.kp = 1.5
```

This allows mission-specific tuning without changing the base code.
