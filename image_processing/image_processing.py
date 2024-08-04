import os
import datetime
import random
import cv2
import base64
import numpy as np
import base64

from deepface import DeepFace
from gaze_tracking.gaze_tracking import GazeTracking

os.chdir(os.path.dirname(os.path.abspath(__file__))) # TODO: remove

class ImageProcessor:
    def __init__(self):
        self.gaze_tracker = GazeTracking()
        print("Image Processor Initialized")

    def gaze_region(self, height, width, left_pupil, right_pupil):
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
            return [3, 3]
            
        left_region = 1 if is_inner_region(left_pupil) else 2
        right_region = 1 if is_inner_region(right_pupil) else 2

        return [left_region, right_region]

    def gaze_processor(self, image=None):
        # decoded_data = base64.b64decode(image)
        # nparr = np.frombuffer(decoded_data, np.uint8) # already turnt into nparr in caller func
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        self.gaze_tracker.refresh(image)
        # height, width, _ = image.shape
        # left_pupil_pos = self.gaze_tracker.pupil_left_coords()
        # right_pupil_pos = self.gaze_tracker.pupil_right_coords()
        # region = self.gaze_region(height, width, left_pupil_pos, right_pupil_pos)

        if self.gaze_tracker.is_up():
            gaze_direction = "up"
        elif self.gaze_tracker.is_down():
            gaze_direction = "down"
        elif self.gaze_tracker.is_right():
            gaze_direction = "right"
        elif self.gaze_tracker.is_left():
            gaze_direction = "left"
        elif self.gaze_tracker.is_center():
            gaze_direction = "center"
        else:
            gaze_direction = "off" # deem as off screen

        return gaze_direction

    def process_image(self, image=None):
        # grab locally # TODO replace
        # facial expression to extract dominant expression
        
        data = {}
        decoded_data = base64.b64decode(image)
        nparr = np.frombuffer(decoded_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        try:
            analysis = DeepFace.analyze(img_path=image, actions=["emotion"])
            dominant_emotion = analysis[0]["dominant_emotion"]
            print(dominant_emotion)
        except:
            dominant_emotion = None
        
        data["dominant_emotion"] = dominant_emotion

        # try:
        #     ...
        # except:
        #       data["gaze_area"] = 3
        try:
            data["gaze_area"] = self.gaze_processor(nparr)
        except:
            data["gaze_area"] = "off"

        return data

        

        # eye gaze to determine general direction of eyes and X, Y coordinates    

        # TODO: add try catch -> return None if no face detected




class DataAggregator:
    def __init__(self, study_session_id):
        self.study_session_id = study_session_id
        self.image_processor = ImageProcessor()
        self.emotions = set(["sad", "angry", "surprise", "fear", "happy",
            "disgust", "neutral"])
        self.gaze_areas = set(["up", "down", "left", "right", "center", "offs"]) # 1 for center, 2 for outer rim, 3 for off screen
        self.weights = {
            "happy": 0.3,
            "neutral": 1,
            "surprised": 0.3,
            "fear": 0.1,
            "angry": 0.2,
            "sad": 0.3,
            "disgust": 0.1,
            "up": 0.9,
            "center": 1,
            "down": 0.7, 
            "left": 0.35,
            "right": 0.2,
            "off": 0
        }

    def grab_images(self):
        # TODO: connect to db and grab all images under self.study_session_id
        with open("./test_images/kevin_neutral_5.jpg", "rb") as image:
            image_data = image.read()
            base64_encoded = base64.b64encode(image_data)
        return [{"base64_encoded": base64_encoded, "timestamp": datetime.datetime(2024, 7, 26, 15, 30, 00)}]

    def process_single_image(self, image=None):
        image_data = self.image_processor.process_image(image)
        return image_data
        # aggregate
    
    def process_images(self):
        images = self.grab_images()
        # sort images by timestamp
        all_buckets = []

        # for each bucket, process images for up to 10 seconds after that buckets duration
        bucket_start_time = None
        bucket_data = []
        for image in images:
            if bucket_start_time and image.timestamp > bucket_start_time + datetime.timedelta(seconds=10):
                aggregated_bucket = self.aggregate_bucket(bucket_data)
                all_buckets.append(aggregated_bucket)
                bucket_start_time = None
                bucket_data = []

            
            if not bucket_start_time:
                bucket_start_time = image["timestamp"] # TODO: replace with actual timestamp
            image_data = self.process_single_image(image["base64_encoded"]) # TODO: replace with image
            image_data["timestamp"] = image["timestamp"]
            bucket_data.append(image_data)

        # process the last bucket
        aggregated_bucket = self.aggregate_bucket(bucket_data)
        all_buckets.append(aggregated_bucket)

        return all_buckets
    

    def aggregate_bucket(self, bucket):
        if not bucket:
            return None
        
        start_timestamp = bucket[0]["timestamp"] # should be sorted by timestamp
        emotion_count = {emotion: 0 for emotion in self.emotions}
        gaze_area_count = {gaze_id: 0 for gaze_id in self.gaze_areas}
        for data in bucket:
            dominant_emotion = data["dominant_emotion"]
            gaze_area = data["gaze_area"]
            if dominant_emotion in emotion_count:
                emotion_count[dominant_emotion] += 1
            if gaze_area in gaze_area_count:
                gaze_area_count[gaze_area] += 1
        

        face_data = {"dominant_emotions": emotion_count, "gaze_area": gaze_area_count}
        fitness = self.determine_fitness(face_data)
        
        processed_image = {"face_data": face_data, "focus": fitness, "timestamp": start_timestamp}
        return processed_image

    def determine_fitness(self, bucket):
        # calculate weighted average
        emotion_count = bucket["dominant_emotions"]
        gaze_area_count = bucket["gaze_area"]
        fitness = 0

        total_emotion_count = sum(emotion_count.values())
        total_gaze_area_count = sum(gaze_area_count.values())
        for emotion, count in emotion_count.items():
            fitness += 0.7 * self.weights.get(emotion, 0) * count / total_emotion_count

        for gaze, count in gaze_area_count.items():
            fitness += 0.3 * self.weights.get(gaze, 0) * count / total_gaze_area_count

        # penalize if theres "spread out" freq. eg. dont penalize 1 1 1 3 2 but penalize 1 1 2 3 4 5
        max_emotion_count = max(emotion_count.values())
        if max_emotion_count < 0.4 * total_emotion_count:
            fitness -= (total_emotion_count - max_emotion_count) * 0.2

        max_gaze_count = max(gaze_area_count.values())
        if max_gaze_count < 0.4 * total_gaze_area_count:
            fitness -= (total_gaze_area_count - max_gaze_count) * 0.2

        return max(1, fitness*10)
        

    

func = DataAggregator(1)
print(func.process_images())

"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""


# from dataclasses import dataclass

# class GazeData:
#     left_pupil: tuple
#     right_pupil: tuple
#     gaze_direction: str

# def gaze_region(height, width, left_pupil, right_pupil):
#     """Returns the general region in which the pupil's are gazing at"""
#     inner_x_min = width * 0.2
#     inner_x_max = width * 0.8
#     inner_y_min = height * 0.2
#     inner_y_max = height * 0.8

#     def is_inner_region(pupil):
#         if pupil is None:
#             return False
#         x, y = pupil
#         return inner_x_min <= x <= inner_x_max and inner_y_min <= y <= inner_y_max
    
#     if (left_pupil == None and right_pupil == None):
#         return ["A3", "A3"]
        
#     left_region = "A1" if is_inner_region(left_pupil) else "A2"
#     right_region = "A1" if is_inner_region(right_pupil) else "A2"

#     return [left_region, right_region]

# gaze = GazeTracking()
# # webcam = cv2.VideoCapture(0)


# # Load the image
# image_path = "./bottom-right.jpg" # if image is empty, it'll give a cv2.error with !_src.empty() for 'cvtColor'

# with open(image_path, "rb") as image_file:
#     # Convert image to base64
#     base64_image = base64.b64encode(image_file.read()).decode('utf-8')

# # Decode the base64 image back to a numpy array
# decoded_data = base64.b64decode(base64_image)
# nparr = np.frombuffer(decoded_data, np.uint8)
# frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

# # frame = cv2.imread(image_path)
# height, width, _ = frame.shape
# #A1 = inner 80% of screen, A2 = outer 20% of screen, A3 = off screen (no ouput from eye image)

# gaze.refresh(frame)

# if gaze.is_blinking():
#     gaze_direction = "Blinking"
# elif gaze.is_right() and gaze.is_up():
#     gaze_direction = "Looking top-right"
# elif gaze.is_right() and gaze.is_down():
#     gaze_direction = "Looking bottom-right"
# elif gaze.is_right() and not gaze.is_up() and not gaze.is_down():
#     gaze_direction = "Looking right"
# elif gaze.is_left() and gaze.is_up():
#     gaze_direction = "Looking top-left"
# elif gaze.is_left() and gaze.is_down():
#     gaze_direction = "Looking bottom-left"
# elif gaze.is_left() and not gaze.is_up() and not gaze.is_down():
#     gaze_direction = "Looking left"
# elif gaze.is_down() and not gaze.is_left() and not gaze.is_right():
#     gaze_direction = "Looking down"
# elif gaze.is_up() and not gaze.is_left() and not gaze.is_right():
#     gaze_direction = "Looking up"
# elif gaze.is_center():
#     gaze_direction = "Looking center"
# else:
#     gaze_direction = "Cannot determine gaze direction"

# # Get coordinates of left and right pupil
# left_pupil_pos = gaze.pupil_left_coords()
# right_pupil_pos = gaze.pupil_right_coords()
# region = gaze_region(height, width, left_pupil_pos, right_pupil_pos)

# # gaze_data = [left_pupil_pos, right_pupil_pos, gaze_direction, region]

# gaze_data = {
#     "pupil_coordinates" : {
#         "left_pupil_pos": left_pupil_pos,
#         "right_pupil_pos": right_pupil_pos,
#     },
#     "gaze_direction": gaze_direction,
# }

# print(gaze_data)