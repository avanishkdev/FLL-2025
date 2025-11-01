# Robot Tuning Guide

This guide covers testing and tuning procedures for the robot control package.

## Quick Start Checklist

- [ ] Verify hardware connections (ports A, B, C)
- [ ] Test individual motors forward/backward
- [ ] Calibrate gyro (reset on flat surface)
- [ ] Test straight driving over known distance
- [ ] Test turning to known angles
- [ ] Tune PID parameters if needed
- [ ] Test full mission sequence

## Hardware Verification

### 1. Motor Direction Test
```python
# Test each motor individually
left_motor.hw.run(500)   # Should rotate forward
right_motor.hw.run(500)  # Should rotate forward
```

Verify:
- Motors rotate in expected direction
- Encoders count up when driving forward
- No mechanical binding

### 2. Gyro Calibration
- Place robot on flat, stable surface
- Reset gyro: `hub.imu.reset_heading(0)`
- Verify reading: `hub.imu.angle()` should be near 0
- Manually rotate robot 90° clockwise, verify reading is ~90

## Movement Testing

### 3. Straight Driving
Test with known distances:
```python
drive.drive_straight(500, speed=50)  # 500mm forward
```

Measure actual distance traveled and compare. Adjust if needed:
- If undershooting: Check wheel diameter setting
- If drifting: Verify gyro calibration and heading PID gains

### 4. Turning
Test with known angles:
```python
drive.turn_to(90, speed=40)   # Turn to 90°
drive.turn_to(0, speed=40)    # Return to 0°
```

Verify:
- Turns are accurate (±2-3 degrees acceptable)
- Robot stops smoothly without overshoot
- Consistent in both directions

## PID Tuning

### Heading Control (for straight driving)
Located in `DriveController.__init__`:
```python
self.heading_pid = PID(kp=1.5, ki=0.0, kd=0.1, integral_limit=20)
```

**Symptoms and adjustments:**
- **Snaking/oscillation**: Reduce `kp`, increase `kd`
- **Slow correction**: Increase `kp`
- **Steady-state error**: Add small `ki` (0.01-0.05)

### Turn Control
Simple proportional control in `turn_to()`:
```python
turn_speed = clamp(error * 0.8, -speed, speed)
```

**Adjustments:**
- **Overshooting**: Reduce gain (0.8 → 0.6)
- **Slow turns**: Increase gain (0.8 → 1.0)

## Speed Tuning

### Default Speeds
- Straight driving: 40-50 (conservative for accuracy)
- Turning: 40-50
- Maximum: 100 (full speed)

**Speed considerations:**
- Higher speeds: Faster but less accurate
- Lower speeds: More accurate but slower
- Deceleration distance: Adjust `decel_distance_mm` parameter

### Deceleration Tuning
In `drive_straight()`:
```python
decel_distance_mm=100  # Start slowing 100mm before target
```

Adjust based on:
- Robot mass and momentum
- Surface friction
- Desired stopping accuracy

## Mission-Specific Testing

### Test Sequence
1. **Isolated movements**: Test each drive/turn individually
2. **Segment testing**: Test 2-3 moves in sequence
3. **Full mission**: Run complete mission from start
4. **Consistency check**: Run mission 3-5 times

### Common Issues

**Robot veers during straight driving:**
- Check wheel wear/damage
- Verify motor calibration
- Adjust heading PID gains

**Inconsistent turning:**
- Recalibrate gyro on flat surface
- Check for loose connections
- Verify battery charge (low voltage affects performance)

**Jerky movement:**
- Reduce speeds
- Increase deceleration distance
- Check for mechanical friction

## Parameter Reference

### Robot Configuration
```python
WHEEL_DIAMETER_MM = 56    # Measured wheel diameter
WHEEL_BASE_MM = 80        # Distance between wheel centers
TICKS_PER_REV = 360       # Encoder resolution
MAX_DEG_PER_SEC = 1080    # Motor maximum speed
```

### Control Parameters
```python
# Heading PID (navigation.py)
kp = 1.5          # Proportional gain
ki = 0.0          # Integral gain
kd = 0.1          # Derivative gain

# Turn control (navigation.py)
turn_gain = 0.8   # Proportional gain for turning
tolerance = 2     # Acceptable angle error (degrees)

# Straight driving
decel_distance_mm = 100   # Deceleration start distance
distance_tolerance = 5    # Distance error threshold (mm)
```

## Best Practices

1. **Always test on competition surface** - Mat friction differs from smooth floors
2. **Fresh batteries** - Use fully charged batteries for consistent performance
3. **Warmup runs** - Run test sequences before competition attempts
4. **Document changes** - Note all parameter adjustments
5. **Incremental tuning** - Change one parameter at a time
6. **Verify repeatability** - Test changes 3-5 times

## Troubleshooting

| Problem | Possible Causes | Solutions |
|---------|----------------|-----------|
| Robot won't move | Motor connections, battery | Check ports, recharge battery |
| Erratic movement | Gyro drift, loose parts | Recalibrate, check mounting |
| Inaccurate distances | Wrong wheel diameter | Measure and update constant |
| Turns overshoot | High gain, high speed | Reduce turn_gain or speed |
| Oscillation in straight | High heading kp | Reduce kp, increase kd |

## Advanced Tuning

For mission-specific optimizations:
1. Profile each movement's actual vs. expected performance
2. Adjust speeds for time-critical vs. accuracy-critical segments
3. Consider separate PID parameters for different mission phases
4. Test edge cases (sharp turns, long distances, obstacles)

## Contact & Support

For issues or questions about the robot package, refer to:
- Package documentation: `robot/README.md`
- Code comments in source files
- Team documentation and notes
