# Gesture-Volume-Control

This project concerns itself with volume control via gesture recognition. The idea behind the project is to set volume according to the distance between the thumb and index fingertips. To assist with this project two open-source libraries ```MediaPipe``` and ```Pycaw``` have been used for hand pose estimation and volume interaction respectively.

## Programme features

To avoid mistakenly setting the volume by a random amount, it is required for the user to have their pinky finger lowered before any volume adjustments can be made. To implement this the y-coordinate of the pinky finger pose is compared against the lower two joints and if it is smaller than these two the finger is deemed to be lowered.

Once the volume has been set the programme can be closed via pressing the 'Esc' key or putting down the middle finger in a similar manner to the pinky. To avoid mistakenly closing the programme when the hand enters the scene, a 3-second timer is started as soon as the hand enters the frame, and only after these 3 seconds can the programme be closed using the middle finger.

A bounding box is placed around the detected hand and the area (in pixels) of this box is calculated. To prioritise hands in the foreground of the video, a constraint is placed upon this area where if the area of a bounding box is below a certain amount the hand will not be detected

To use this model make sure all .py scripts are installed and placed in the same directory. Make sure the following libraries are installed: ```numpy```,```pycaw```,```mediapipe```,```cv2```. Once all scripts and required packages are installed, open the Final.py script and run it.
