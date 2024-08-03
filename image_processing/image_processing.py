import os
from deepface import DeepFace

os.chdir(os.path.dirname(os.path.abspath(__file__))) # TODO: remove

class FacialExpressionRecognition:
    def __init__(self):
        print("hi")

    def process_image(self, image=None):
        # grab locally # TODO replace
        analysis = DeepFace.analyze(img_path="./test_images/girl_long_hair_4.png", actions=["emotion"])
        dominant_emotion = analysis[0]["dominant_emotion"]
        print(dominant_emotion)
        return dominant_emotion
        # TODO: add try catch -> return None if no face detected


test = FacialExpressionRecognition()
test.process_image()


class DataAggregator:
    def __init__(self, study_session_id):
        self.study_session_id = study_session_id
        self.image_processor

    def grab_images(self):
        # TODO: connect to db and grab all images under self.study_session_id

    def process