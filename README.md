# Gesture-Volume-Control

This project concerns itself with volume control via gesture recognition. The idea behind the project is to set volume according to the distance between the thumb and index fingertips. To assist with this project two open-source libraries ```MediaPipe``` and ```Pycaw``` have been used for hand pose estimation and volume interaction respectively.

To avoid mistakenly setting the volume by a random amount, it is required for the user to have their pinky finger lowered before any volume adjustments can be made. To implement this the y-coordinate of the pinky finger pose is compared against the lower two joints and if it is smaller than these two the finger is deemed to be lowered.
