"""
robot_helpers.py
A helper library to centralize DriveBase and manipulator settings and provide predictable movement helpers.
"""
from pybricks.hubs import PrimeHub
from pybricks.parameters import Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import wait

class Robot:
    def __init__(
        self,
        left_port=Port.A,
        right_port=Port.C,
        manip_port=Port.B,
        left_dir=Direction.COUNTERCLOCKWISE,
        right_dir=Direction.CLOCKWISE,
        manip_dir=Direction.CLOCKWISE,
        wheel_diameter=56,
        axle_track=80,
    ):
        self.hub = PrimeHub()
        self.left = Motor(left_port, left_dir)
        self.right = Motor(right_port, right_dir)
        self.manip = Motor(manip_port, manip_dir)
        self.drive = DriveBase(self.left, self.right, wheel_diameter, axle_track)

        # Enable gyro and reset odometry where possible
        try:
            self.drive.use_gyro(True)
            self.drive.reset(0, 0)
        except Exception:
            pass
        try:
            self.left.reset_angle(0)
        except Exception:
            pass

        self.set_precision_mode()

    def set_precision_mode(self):
        self.drive.settings(
            straight_speed=220,
            straight_acceleration=1200,
            turn_rate=90,
            turn_acceleration=200,
        )

    def set_travel_mode(self):
        self.drive.settings(
            straight_speed=600,
            straight_acceleration=3000,
            turn_rate=150,
            turn_acceleration=400,
        )

    def precise_straight(self, distance_mm, speed=None, settle_ms=200):
        if speed is not None:
            self.drive.settings(straight_speed=speed)
        self.drive.straight(distance_mm)
        wait(settle_ms)

    def precise_turn(self, angle_deg, turn_rate=None, settle_ms=150):
        if turn_rate is not None:
            self.drive.settings(turn_rate=turn_rate)
        self.drive.turn(angle_deg)
        wait(settle_ms)

    def run_manipulator(self, speed, angle, brake=Stop.BRAKE):
        self.manip.run_angle(speed, angle, brake)

    def stop(self):
        try:
            self.drive.stop()
        except Exception:
            pass

    # aliases
    def straight(self, mm, speed=None):
        return self.precise_straight(mm, speed)

    def turn(self, deg, turn_rate=None):
        return self.precise_turn(deg, turn_rate)
