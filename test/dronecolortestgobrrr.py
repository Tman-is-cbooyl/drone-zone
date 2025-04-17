import keyboard
import cv2
import threading
from time import sleep
from djitellopy import Tello
import numpy as np

# Initialize the drone
drone = Tello()

# Function to detect dominant colors
def detect_colors(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    color_ranges = {
        "Red": ((0, 120, 70), (10, 255, 255)),
        "Green": ((36, 25, 25), (86, 255, 255)),
        "Blue": ((94, 80, 2), (126, 255, 255)),
        "Yellow": ((25, 50, 50), (35, 255, 255)),
        "Orange": ((10, 100, 20), (25, 255, 255)),
    }

    detected_colors = []

    for color_name, (lower, upper) in color_ranges.items():
        lower_bound = np.array(lower)
        upper_bound = np.array(upper)

        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        if np.count_nonzero(mask) > 0:
            detected_colors.append(color_name)

    return detected_colors

# Function to display the camera feed with color detection
def show_camera():
    color_ranges = {
        "Red": ((0, 120, 70), (10, 255, 255)),
        "Orange": ((10, 100, 20), (25, 255, 255)),
        "Yellow": ((25, 50, 50), (35, 255, 255)),
        "Green": ((36, 25, 25), (86, 255, 255)),
        "Blue": ((94, 80, 2), (126, 255, 255)),
        "Purple": ((125, 50, 50), (155, 255, 255))
    }

    key_to_color = {
        '1': 'Red',
        '2': 'Orange',
        '3': 'Yellow',
        '4': 'Green',
        '5': 'Blue',
        '6': 'Purple'
    }

    check_logged = False

    while True:
        frame = drone.get_frame_read().frame
        if frame is not None:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Check for color detection based on key press (1-6)
            for key, color_name in key_to_color.items():
                if keyboard.is_pressed(key) and not check_logged:
                    lower, upper = color_ranges[color_name]
                    mask = cv2.inRange(hsv, np.array(lower), np.array(upper))

                    if np.count_nonzero(mask) > 0:
                        print(f"{color_name} detected!")
                        with open("detected_colors.txt", "a") as file:
                            file.write(f"{color_name} detected!\n")
                    else:
                        print(f"{color_name} not found.")

                    check_logged = True  # Avoid multiple triggers
                    sleep(0.3)  # Debounce delay

            # Reset logging if no key is pressed
            if not any(keyboard.is_pressed(k) for k in key_to_color):
                check_logged = False

            cv2.imshow("Tello Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('y'):
            break

    cv2.destroyAllWindows()

# Main Program
try:
    drone.connect()
    battery = drone.get_battery()

    if battery == 0:
        raise Exception("Drone connection failed. Battery is at 0%.")
    print(f"Battery Level: {battery}%")

    # Check if the drone is ready for takeoff
    print("Preparing to take off...")
    drone.takeoff()
    sleep(1)  # Wait a bit after takeoff to ensure stability

    print("Drone has taken off.")
    
    # Start the camera stream
    drone.streamon()  

    # Start camera display in a separate thread
    camera_thread = threading.Thread(target=show_camera, daemon=True)
    camera_thread.start()

    print("Use W, A, S, D to move, SPACE to go up, CTRL to go down.")
    print("Use Q to rotate counterclockwise, E to rotate clockwise.")
    print("Press ESC to land and exit. Press Y to close the camera window.")
    
    # Main control loop
    while True:
        if keyboard.is_pressed('ctrl'):
            drone.send_rc_control(0, 0, 0, 0)  # Emergency stop

        elif keyboard.is_pressed('w'):
            drone.send_rc_control(0, 20, 0, 0)
        elif keyboard.is_pressed('a'):
            drone.send_rc_control(-20, 0, 0, 0)
        elif keyboard.is_pressed('s'):
            drone.send_rc_control(0, -20, 0, 0)
        elif keyboard.is_pressed('d'):
            drone.send_rc_control(20, 0, 0, 0)
        elif keyboard.is_pressed('space'):
            drone.send_rc_control(0, 0, 20, 0)
        elif keyboard.is_pressed('shift'):
            drone.send_rc_control(0, 0, -20, 0)
        elif keyboard.is_pressed('q'):
            drone.rotate_counter_clockwise(45)
        elif keyboard.is_pressed('e'):
            drone.rotate_clockwise(45)
        elif keyboard.is_pressed('c'):
            drone.rotate_clockwise(360)
        elif keyboard.is_pressed('v'):
            drone.rotate_counter_clockwise(360)
        elif keyboard.is_pressed('z'):
            drone.flip_back()
        elif keyboard.is_pressed('esc'):
            print("Landing...")
            break

        sleep(0.1)

except Exception as e:
    print(f"Error: {e}")

finally:
    drone.streamoff()  # Stop video stream
    if drone.is_flying:
        drone.land()
    drone.end()
    print("Drone safely landed and connection closed.")
