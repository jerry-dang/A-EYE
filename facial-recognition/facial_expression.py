import os
from deepface import DeepFace

os.chdir(os.path.dirname(os.path.abspath(__file__))) # TODO: remove

class FacialExpressionRecognition:
    def __init__(self):
        print("hi")

    def process_image(self):
        # grab locally # TODO replace
        analysis = DeepFace.analyze(img_path="./test_images/leo_neutral.jpg", actions=["emotion"])
        dominant_emotion = analysis[0]["dominant_emotion"]
        print(dominant_emotion)
        return dominant_emotion
        # TODO: add try catch -> return None if no face detected


test = FacialExpressionRecognition()
test.process_image()
