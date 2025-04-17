Team members: 

Tony Coggins, Alex Ecker, Kaiden Ecker



Project Overview: 

Our project uses a DJI Tello drone and openCV to detect and log colors from the drone's live camera. It supports real time streaming, manual control of the drone using a keyboard, and color logging by simply pressing a pixl on the video camera feed with a mouse. The detected colors are then saved to a text file if needed for further analysis.



System:

1.Connect to the Tello drone and check battery level.

2.Execute takeoff sequence and start camera stream.

3.OpenCV window displays the live video feed.

4.Colors are detected in real time using HSV ranges.

5.Pressing F logs the detected colors to detected_colors.txt.

6.Use the keyboard to move or rotate the drone.

7.Press ESC to land and safely shut down the system.



Supported Colors and Ranges:

Red: 
    -Hue: 0-10
    -Saturation 120-255
    -Value: 70-255

Orange: 
    -Hue: 10-25
    -Saturation 100-255
    -Value: 20-255

Yellow: 
    -Hue: 25-35
    -Saturation 50-255
    -Value: 50-255

Green: 
    -Hue: 36-86
    -Saturation 25-255
    -Value: 25-255

Blue: 
    -Hue: 94-126
    -Saturation 80-255
    -Value: 2-255

Purple: 
    -Hue: 127-160
    -Saturation 80-255
    -Value: 20-255



KeyBoard Controls:

W- Forward

A- Left

S- Backward

D- Right

Space- Up

Shift- Down

Q- Rotate counter-clockwise

E- Rotate clockwise

C- 360 degree clockwise

V- 360 counter-clockwise

Z- Flip backward

F- log colors to file

Esc- Land and exit program