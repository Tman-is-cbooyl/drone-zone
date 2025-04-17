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
    # Convert the frame to HSV (Hue, Saturation, Value) color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define color ranges in HSV space
    color_ranges = {
        "Red": ((0, 120, 70), (10, 255, 255)),
        "Green": ((36, 25, 25), (86, 255, 255)),
        "Blue": ((94, 80, 2), (126, 255, 255)),
        "Yellow": ((25, 50, 50), (35, 255, 255)),
        "Orange": ((10, 100, 20), (25, 255, 255)),
    }

    detected_colors = []

    # Loop over each color range and check if the color is present
    for color_name, (lower, upper) in color_ranges.items():
        lower_bound = np.array(lower)
        upper_bound = np.array(upper)

        # Mask the frame with the color range
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        # If the mask contains any non-zero values, the color is present
        if np.count_nonzero(mask) > 0:
            detected_colors.append(color_name)

    return detected_colors

# Function to display the camera feed
# Mouse callback function to detect color at clicked point
def click_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        frame = param['frame']
        if frame is not None:
            b, g, r = frame[y, x]
            color = f'R={r}, G={g}, B={b}'
            print(f"Clicked at ({x},{y}) - Color: {color}")
            cv2.rectangle(frame, (x, y - 20), (x + 150, y), (0, 0, 0), -1)
            cv2.putText(frame, color, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

# Function to display the camera feed with color detection
def show_camera():
    color_logged = False
    params = {'frame': None}
    cv2.namedWindow("Tello Camera")
    cv2.setMouseCallback("Tello Camera", click_color, params)

    while True:
        frame = drone.get_frame_read().frame
        if frame is not None:
            params['frame'] = frame.copy()  # Pass a copy to avoid draw-on-frame issues
            detected_colors = detect_colors(frame)

            # Log on 'F' key press
            if keyboard.is_pressed('f') and not color_logged:
                if detected_colors:
                    print(f"Detected Colors: {', '.join(detected_colors)}")
                    with open("detected_colors.txt", "a") as file:
                        file.write(f"Detected Colors: {', '.join(detected_colors)}\n")
                    color_logged = True

            if not keyboard.is_pressed('f'):
                color_logged = False

            cv2.imshow("Tello Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('y'):
            break

    cv2.destroyAllWindows()


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
            drone.send_rc_control(0, 25, 0, 0)
        elif keyboard.is_pressed('a'):
            drone.send_rc_control(-25, 0, 0, 0)
        elif keyboard.is_pressed('s'):
            drone.send_rc_control(0, -25, 0, 0)
        elif keyboard.is_pressed('d'):
            drone.send_rc_control(25, 0, 0, 0)
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
