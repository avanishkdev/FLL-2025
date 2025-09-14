from pybricks.hubs import PrimeHub
from pybricks.parameters import Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# Hub (for gyro)
hub = PrimeHub()

# Motors
right = Motor(Port.C, Direction.CLOCKWISE)
left = Motor(Port.A, Direction.COUNTERCLOCKWISE)
left_gear = Motor(Port.B, Direction.COUNTERCLOCKWISE)
robot = DriveBase(left, right, wheel_diameter=56, axle_track=98)

# Settings (slow = more precise)
robot.settings(
    straight_speed=150,         # mm/s
    straight_acceleration=120,
    turn_rate=90,               # deg/s
    turn_acceleration=60
)

# Reset gyro before starting
hub.imu.reset_heading(0)


# ----------------- Gyro helpers -------------------
def drive_straight(distance_mm, speed=150):
    """Drive straight while correcting heading drift using gyro."""
    start_angle = hub.imu.heading()
    robot.reset()
    robot.stop()
    robot.straight(0)  # make sure stopped

    robot.stop()
    robot.reset()
    robot.stop()

    # Drive in small steps while correcting heading
    step = 20  # mm step
    moved = 0
    while abs(moved) < abs(distance_mm):
        remaining = distance_mm - moved
        step_dist = step if abs(remaining) > step else remaining

        # correction factor
        error = hub.imu.heading() - start_angle
        correction = -1.2 * error  # simple proportional gain

        # drive step with correction
        robot.drive(speed, correction)
        wait(50)

        moved = robot.distance()

    robot.stop(Stop.BRAKE)


def turn_to(angle_target, speed=90):
    """Turn robot to a specific absolute angle (degrees)."""
    # angle_target is relative to start (0 after reset)
    kp = 2.0
    while True:
        error = angle_target - hub.imu.heading()
        if abs(error) < 1:  # within 1° tolerance
            break
        turn_rate = max(min(kp * error, speed), -speed)
        robot.drive(0, turn_rate)
        wait(20)
    robot.stop(Stop.BRAKE)


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
