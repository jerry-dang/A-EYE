import os
import datetime
import random
from deepface import DeepFace

os.chdir(os.path.dirname(os.path.abspath(__file__))) # TODO: remove

class ImageProcessor:
    def __init__(self):
        print("Image Processor Initialized")

    def process_image(self, image=None):
        # grab locally # TODO replace
        # facial expression to extract dominant expression
        data = {}
        try:
            analysis = DeepFace.analyze(img_path="./test_images/girl_long_hair_4.png", actions=["emotion"])
            dominant_emotion = analysis[0]["dominant_emotion"]
            print(dominant_emotion)
        except:
            dominant_emotion = None
        
        data["dominant_emotion"] = dominant_emotion

        # try:
        #     ...
        # except:
        #       data["gaze_area"] = 3
        data["gaze_area"] = random.randint(1, 3)

        return data

        

        # eye gaze to determine general direction of eyes and X, Y coordinates    

        # TODO: add try catch -> return None if no face detected




class DataAggregator:
    def __init__(self, study_session_id):
        self.study_session_id = study_session_id
        self.image_processor = ImageProcessor()
        self.emotions = set(["sad", "angry", "surprise", "fear", "happy",
            "disgust", "neutral"])
        self.gaze_areas = set([1, 2, 3]) # 1 for center, 2 for outer rim, 3 for off screen

    def grab_images(self):
        # TODO: connect to db and grab all images under self.study_session_id
        return [{"timestamp": datetime.datetime(2024, 7, 26, 15, 30, 00)}]

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
            image_data = self.process_single_image(None) # TODO: replace with image
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
        

        face_data = {"dominant_emotions": emotion_count, "gaze_area": gaze_area_count, "timestamp": start_timestamp}
        return face_data
    

func = DataAggregator(1)
print(func.process_images())