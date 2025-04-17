from djitellopy import Tello
import cv2
import numpy as np
import keyboard
import threading
import time
import frame
# Initialize drone
tello = Tello()
tello.connect()
print(f"Battery: {tello.get_battery()}%")

cropped_frame = frame[0:100, 0:100]

# States
movement = {'forward': 0, 'backward': 0, 'left': 0, 'right': 0, 'up': 0, 'down': 0, 'yaw_left': 0, 'yaw_right': 0}
speed = 0
camera_on = False
stream_thread = None

# Movement loop
def update_movement():
    global speed
    while True:
        lr = movement['right'] - movement['left']
        fb = movement['forward'] - movement['backward']
        ud = movement['up'] - movement['down']
        yaw = movement['yaw_right'] - movement['yaw_left']
        tello.send_rc_control(lr * speed, fb * speed, ud * speed, yaw * speed)
        time.sleep(0.05)
        if any(v != 0 for v in movement.values()):
            speed = min(speed + 1, 100)
        else:
            speed = 0

threading.Thread(target=update_movement, daemon=True).start()

# Color detection
def detect_colors(frame):
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

active_color = None  # Start with no filtering 

for key, color in key_to_color.items():
    if keyboard.is_pressed(key):
        if active_color == color:
            active_color = None  # Turn off if already selected
        else:
            active_color = color
        sleep(0.3)  # Debounce

if active_color:
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower, upper = color_ranges[active_color]
    mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
    colored = cv2.bitwise_and(frame, frame, mask=mask)

    # Grayscale background
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_3ch = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    # Combine masked color with grayscale
    frame = np.where(mask[:, :, np.newaxis] == 0, gray_3ch, colored)

    # Add a label for current color
    cv2.putText(frame, f"{active_color} Mode", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

def save_colors_to_file(colors):
    with open("detected_colors.txt", "a") as f:
        f.write(", ".join(colors) + "\n")

# Start/stop camera
def toggle_camera():
    global camera_on, stream_thread
    if camera_on:
        tello.streamoff()
        camera_on = False
    else:
        tello.streamon()
        camera_on = True

        def stream_loop():
            frame_read = tello.get_frame_read()
            while camera_on:
                frame = frame_read.frame
                cv2.imshow("Tello Camera", frame)
                if cv2.waitKey(1) == ord('x'):
                    break
            cv2.destroyAllWindows()

        stream_thread = threading.Thread(target=stream_loop)
        stream_thread.start()

# Keyboard input
def on_press(key):
    try:
        k = key.char.lower()
        if k == 'w':
            movement['forward'] = 1
        elif k == 's':
            movement['backward'] = 1
        elif k == 'a':
            movement['left'] = 1
        elif k == 'd':
            movement['right'] = 1
        elif k == 'r':
            movement['up'] = 1
        elif k == 'f':
            movement['down'] = 1
        elif k == 'q':
            movement['yaw_left'] = 1
        elif k == 'e':
            movement['yaw_right'] = 1
        elif k == 'z':
            toggle_camera()
        elif k == 'c':
            if not camera_on:
                tello.streamon()
                time.sleep(1)
            frame = tello.get_frame_read().frame
            found = detect_colors(frame)
            print("Colors detected:", found)
            save_colors_to_file(found)
    except AttributeError:
        pass

def on_release(key):
    try:
        k = key.char.lower()
        if k == 'w':
            movement['forward'] = 0
        elif k == 's':
            movement['backward'] = 0
        elif k == 'a':
            movement['left'] = 0
        elif k == 'd':
            movement['right'] = 0
        elif k == 'r':
            movement['up'] = 0
        elif k == 'f':
            movement['down'] = 0
        elif k == 'q':
            movement['yaw_left'] = 0
        elif k == 'e':
            movement['yaw_right'] = 0
    except AttributeError:
        pass

# Start keyboard listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    tello.takeoff()
    print("Drone is flying. Press ESC to land and quit.")
    listener.join()

tello.land()
tello.end()