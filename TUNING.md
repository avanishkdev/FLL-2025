# Robot Navigation Tuning Guide

This guide explains how to tune the robot navigation system for optimal performance.

## Quick Start Checklist

Before running missions on the robot:
- [ ] Verify gyro readout by checking `gyro.get_heading()` after rotating robot
- [ ] Test small movements: `drive.turn_to(10)` and `drive.drive_straight(100)`
- [ ] Tune heading PID gains if turns overshoot or oscillate
- [ ] Adjust base_speed if movements are too fast or slow
- [ ] Verify MAX_DEG_PER_SEC if motors sound aggressive or stall

## Key Constants

### Motor Speed Mapping (robot/motors.py)

```python
MAX_DEG_PER_SEC = 1080
```

This maps speed values (-100 to 100) to motor velocities in degrees per second.
- Speed 100 → 1080 deg/s
- Speed 50 → 540 deg/s
- Speed -100 → -1080 deg/s

**Adjust if:** Motors are too aggressive, making loud noises, or stalling under load.
**Recommended range:** 720-1440 deg/s for MAX_DEG_PER_SEC

### Robot Dimensions (robot/navigation.py and pybricks_adapters.py)

```python
wheel_diameter_mm = 56
wheel_base_mm = 80
```

**wheel_diameter_mm:** Diameter of drive wheels in millimeters
- Affects distance calculation accuracy
- Measure actual wheel diameter and update if movements are consistently short/long

**wheel_base_mm:** Distance between left and right wheels
- Affects turn radius calculation
- Measure center-to-center distance between wheel contact points

### Encoder Resolution

```python
ticks_per_rev = 360  # degrees per revolution (built into Pybricks motors)
```

This is fixed for Pybricks motors and should not be changed.

## PID Tuning

### Heading PID (robot/navigation.py - DriveController.__init__)

Controls how the robot maintains heading during turns and straight driving.

```python
self.heading_pid = PID(kp=1.5, ki=0.01, kd=0.1, 
                      output_min=-30, output_max=30)
```

**kp (Proportional):** 1.5
- Increase if robot responds slowly to heading errors
- Decrease if robot oscillates during turns

**ki (Integral):** 0.01
- Increase if robot has steady-state heading error
- Keep small to avoid integral windup

**kd (Derivative):** 0.1
- Increase to reduce overshoot
- Decrease if robot is jittery

**output_min/max:** -30 to 30
- Limits correction power applied to motors
- Increase for more aggressive correction (may cause oscillation)

### Drive PID (robot/navigation.py - DriveController.__init__)

Currently minimal, mainly used for encoder synchronization.

```python
self.drive_pid = PID(kp=0.5, ki=0.0, kd=0.0,
                    output_min=-20, output_max=20)
```

This is intentionally simple. Adjust only if you notice one wheel consistently running faster.

## Speed Settings

### Base Speeds (robot/missions/pybricks_mission_9_pull.py)

```python
drive.drive_straight(180, base_speed=50, timeout_ms=5000)
```

**base_speed:** -100 to 100
- 50 is a conservative default
- Increase for faster missions (60-80)
- Decrease for precision (30-40)

### Turn Speeds (robot/navigation.py - DriveController.turn_to)

```python
base_speed = 30  # Base turning speed
```

**Adjust in code if:**
- Turns are too slow (increase to 40-50)
- Turns overshoot target (decrease to 20-25)

## Testing Procedure

### 1. Verify Gyro

```python
from robot.pybricks_adapters import create_robot_from_mission_9_config

left, right, gyro, manip = create_robot_from_mission_9_config()
gyro.reset_heading(0)
print(gyro.get_heading())  # Should be ~0
# Manually rotate robot 90 degrees clockwise
print(gyro.get_heading())  # Should be ~90
```

### 2. Test Small Turn

```python
from robot.navigation import DriveController

drive = DriveController(left, right, gyro)
drive.reset()
drive.turn_to(10)  # Turn to 10 degrees
# Check if robot turned accurately
```

**If turn overshoots:** Decrease heading_pid.kp to 1.0  
**If turn is too slow:** Increase base_speed in turn_to() to 40

### 3. Test Straight Drive

```python
drive.drive_straight(200, base_speed=50)  # Drive 200mm
# Measure actual distance traveled
```

**If distance is short:** Increase wheel_diameter_mm by 1-2mm  
**If distance is long:** Decrease wheel_diameter_mm by 1-2mm  
**If robot veers:** Check motor directions and wheel alignment

### 4. Full Mission Test

Run the mission and observe:
- Smooth acceleration/deceleration
- Accurate turns
- Consistent straight paths
- No motor stalling

## Common Issues

### Robot oscillates during turns
- **Solution:** Decrease heading_pid.kp (try 1.0 or 0.8)
- **Alternative:** Increase heading_pid.kd (try 0.2)

### Robot doesn't hold straight line
- **Solution:** Increase heading_pid.kp (try 2.0)
- **Check:** Gyro is functioning correctly

### Movements timeout
- **Solution:** Increase base_speed or timeout_ms values
- **Check:** Motors are not stalled or blocked

### Distance accuracy is off
- **Solution:** Measure and update wheel_diameter_mm
- **Formula:** actual_distance = measured_distance × (wheel_diameter_mm / actual_wheel_diameter)

### Motors make loud grinding noise
- **Solution:** Decrease MAX_DEG_PER_SEC to 900 or 720
- **Check:** Wheels move freely and aren't binding

## Advanced Tuning

### Deceleration Curve

In `robot/navigation.py`, the deceleration logic can be adjusted:

```python
if abs(remaining) < abs(distance_deg) * 0.2:  # Last 20% of distance
    current_speed = abs_base_speed * 0.5
```

Change `0.2` (20%) to adjust when deceleration starts:
- Increase to 0.3 for smoother, earlier deceleration
- Decrease to 0.1 for later, more aggressive deceleration

Change `0.5` (50% speed) to adjust deceleration amount:
- Increase to 0.7 for less deceleration
- Decrease to 0.3 for more deceleration

### Tolerance Values

**Turn tolerance** (navigation.py):
```python
tolerance = 2  # Heading tolerance in degrees
```

**Drive tolerance** (navigation.py):
```python
tolerance = 20  # Position tolerance in degrees
```

Tighter tolerances = more accuracy but slower settling time.

## Mission-Specific Tuning

Each mission may need different speed profiles. In your mission file:

```python
# Fast open-field movement
drive.drive_straight(500, base_speed=80, timeout_ms=8000)

# Precise positioning near objectives
drive.drive_straight(50, base_speed=30, timeout_ms=3000)

# Quick turn
drive.turn_to(target, timeout_ms=2000)

# Precise turn
drive.turn_to(target, timeout_ms=5000)  # Longer timeout allows settling
```
