from rest_framework import serializers
from .models import StudySessions, Images, Image_data
import base64
import uuid

class SessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySessions
        fields = ['location', 'start_time', 'end_time', 'noise_level', 'session_id']

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['image_id', 'timestamp', 'user_id', 'session_id', 'binary_encoding']


    def create(self, validated_data):
        base64_image = validated_data.pop('base64_image')
        image_data = base64.b64decode(base64_image)
        image_id = str(uuid.uuid4())  # Generate a new image ID

        # Create the image instance
        image_instance = Images(
            image_id=image_id,
            binary_encoding=image_data,
            **validated_data
        )
        
        # Save the instance to the database
        image_instance.save()
        
        return image_instance
    
class ImageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image_data
        fields = ['face_data', 'timestamp', 'user_id', 'session_id', 'focus_level']
    
    