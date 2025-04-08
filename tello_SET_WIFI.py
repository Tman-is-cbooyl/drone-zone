from djitellopy import Tello
import keyboard
import cv2
import time

# Initialize Tello
drone = Tello()
drone.connect()
print(f"Battery: {drone.get_battery()}%")

# Start video stream
drone.streamon()
drone.takeoff()
time.sleep(2)

print("Controls: W/A/S/D - move, SPACE - up, C - down, Q/E - rotate, ESC - land")

try:
    while True:
        # Show video feed
        frame = drone.get_frame_read().frame
        frame = cv2.resize(frame, (360, 240))
        cv2.imshow("Drone View", frame)
        cv2.waitKey(1)

        # Control keys
        if keyboard.is_pressed("w"):
            drone.move_forward(30)
        elif keyboard.is_pressed("s"):
            drone.move_back(30)
        elif keyboard.is_pressed("a"):
            drone.move_left(30)
        elif keyboard.is_pressed("d"):
            drone.move_right(30)
        elif keyboard.is_pressed("space"):
            drone.move_up(30)
        elif keyboard.is_pressed("c"):  # Using 'c' instead of 'ctrl' for down
            drone.move_down(30)
        elif keyboard.is_pressed("q"):
            drone.rotate_counter_clockwise(45)
        elif keyboard.is_pressed("e"):
            drone.rotate_clockwise(45)
        elif keyboard.is_pressed("esc"):
            print("Landing...")
            break

        time.sleep(0.2)

except Exception as err:
    print(f"Error: {err}")

finally:
    drone.land()
    drone.streamoff()
    drone.end()
    cv2.destroyAllWindows()
    print("Drone safely landed.")
