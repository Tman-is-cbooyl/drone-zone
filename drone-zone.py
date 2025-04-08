# This script is a simple test to test turning
from djitellopy import tello
from time import sleep

main()


def main():
    drone = tello.Tello()
    drone.connect()
    sleep(1)
    # connects and sleeps to ensure it is ready
    sleep(1)
    drone.takeoff()
    sleep(4)
    # Takes off
    drone.move_forward(30)
    sleep(6)
    drone.move_back()
    sleep(6)
    # rotates back and forth
    drone.land()
    # lands
    drone.end()
    