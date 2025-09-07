from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis, Direction, Port
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch


# Set up all devices.
hub = PrimeHub(top_side=Axis.Z, front_side=Axis.X)
left_wheel = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_wheel = Motor(Port.B, Direction.CLOCKWISE)
robot = DriveBase(left_wheel, right_wheel, 56, 114)


# The main program starts here.
robot.straight(250)
hub.imu.reset_heading(0)
wait(200)
robot.turn(95)