from pybricks.hubs import PrimeHub
from pybricks.parameters import Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase

# Hub (for gyro)
hub = PrimeHub()

# Motors
right = Motor(Port.C, Direction.CLOCKWISE)
left = Motor(Port.A, Direction.COUNTERCLOCKWISE)
left_gear = Motor(Port.B, Direction.COUNTERCLOCKWISE)
robot = DriveBase(left, right, wheel_diameter=56, axle_track=98)
robot.use_gyro(True)

# Settings (tuned for smoother accel/decel). Adjust to your robot.
robot.settings(
    straight_speed=160,          # mm/s max cruise speed
    straight_acceleration=300,   # mm/s^2 accel/decel
    turn_rate=120,               # deg/s max turn rate
    turn_acceleration=300        # deg/s^2 accel/decel
)

# Reset gyro before starting
hub.imu.reset_heading(0)


# ----------------- Gyro helpers -------------------
def drive_straight(distance_mm: int) -> None:
    """Drive a precise straight distance using built-in accel/decel and gyro."""
    robot.straight(distance_mm)


def turn_to(angle_target: int) -> None:
    """Turn robot to a specific absolute angle using profiled turn."""
    current = hub.imu.heading()
    delta = angle_target - current
    robot.turn(delta)


def lift():
    left_gear.run_angle(300, 370, then=Stop.BRAKE)
    left_gear.run_angle(300, -359, then=Stop.BRAKE)


# ---------------- Your mission --------------------
# Go forward
drive_straight(735, speed=140)

# Turn right 90
turn_to(90)

# Forward
drive_straight(365, speed=140)

# Turn left 90 (back to 0 heading)
turn_to(0)

# Lift
lift()

# ---------------- Return path ---------------------
# Turn right back to 90
turn_to(90)

# Back 365
drive_straight(-365, speed=140)

# Turn left to face start (0)
turn_to(0)

# Back 735
drive_straight(-735, speed=140)
