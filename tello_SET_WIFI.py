# This script sets the wifi and password on the tello
from djitellopy import tello

drone = tello.Tello()

drone.connect()
# Connects to the drone

drone.set_wifi_credentials('FOOTDRONE1', 'ARMSTRONGISGOATED')
# sets the Wi-Fi ssid and password. Definitely change these to your own.
drone.end()
