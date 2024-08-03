"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
import base64
from gaze_tracking import GazeTracking
import numpy as np
# from dataclasses import dataclass

# class GazeData:
#     left_pupil: tuple
#     right_pupil: tuple
#     gaze_direction: str

def gaze_region(height, width, left_pupil, right_pupil):
    """Returns the general region in which the pupil's are gazing at"""
    inner_x_min = width * 0.2
    inner_x_max = width * 0.8
    inner_y_min = height * 0.2
    inner_y_max = height * 0.8

    def is_inner_region(pupil):
        if pupil is None:
            return False
        x, y = pupil
        return inner_x_min <= x <= inner_x_max and inner_y_min <= y <= inner_y_max
    
    if (left_pupil == None and right_pupil == None):
        return ["A3", "A3"]
        
    left_region = "A1" if is_inner_region(left_pupil) else "A2"
    right_region = "A1" if is_inner_region(right_pupil) else "A2"

    return [left_region, right_region]

gaze = GazeTracking()
# webcam = cv2.VideoCapture(0)


# Load the image
image_path = "./bottom-right.jpg" # if image is empty, it'll give a cv2.error with !_src.empty() for 'cvtColor'

with open(image_path, "rb") as image_file:
    # Convert image to base64
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

# Decode the base64 image back to a numpy array
decoded_data = base64.b64decode(base64_image)
nparr = np.frombuffer(decoded_data, np.uint8)
frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

# frame = cv2.imread(image_path)
height, width, _ = frame.shape
#A1 = inner 80% of screen, A2 = outer 20% of screen, A3 = off screen (no ouput from eye image)

gaze.refresh(frame)

if gaze.is_blinking():
    gaze_direction = "Blinking"
elif gaze.is_right() and gaze.is_up():
    gaze_direction = "Looking top-right"
elif gaze.is_right() and gaze.is_down():
    gaze_direction = "Looking bottom-right"
elif gaze.is_right() and not gaze.is_up() and not gaze.is_down():
    gaze_direction = "Looking right"
elif gaze.is_left() and gaze.is_up():
    gaze_direction = "Looking top-left"
elif gaze.is_left() and gaze.is_down():
    gaze_direction = "Looking bottom-left"
elif gaze.is_left() and not gaze.is_up() and not gaze.is_down():
    gaze_direction = "Looking left"
elif gaze.is_down() and not gaze.is_left() and not gaze.is_right():
    gaze_direction = "Looking down"
elif gaze.is_up() and not gaze.is_left() and not gaze.is_right():
    gaze_direction = "Looking up"
elif gaze.is_center():
    gaze_direction = "Looking center"
else:
    gaze_direction = "Cannot determine gaze direction"

# Get coordinates of left and right pupil
left_pupil_pos = gaze.pupil_left_coords()
right_pupil_pos = gaze.pupil_right_coords()
region = gaze_region(height, width, left_pupil_pos, right_pupil_pos)

# gaze_data = [left_pupil_pos, right_pupil_pos, gaze_direction, region]

gaze_data = {
    "pupil_coordinates" : {
        "left_pupil_pos": left_pupil_pos,
        "right_pupil_pos": right_pupil_pos,
    },
    "gaze_direction": gaze_direction,
}

print(gaze_data)
