from djitellopy import Tello
import cv2

# Initialize the Tello drone
tello = Tello()

# Connect to the Tello drone
tello.connect()

# Start the video stream
tello.streamon()

# Create a named window for the video stream
cv2.namedWindow("Tello Stream", cv2.WINDOW_NORMAL)

try:
    while True:
        # Get the frame from the Tello drone
        frame = tello.get_frame_read().frame

        # Display the frame
        cv2.imshow("Tello Stream", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Release resources
    tello.streamoff()
    cv2.destroyAllWindows()