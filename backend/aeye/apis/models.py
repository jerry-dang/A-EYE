from django.db import models
import uuid

# Create your models here.

class StudySessions(models.Model):
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    noise_level = models.CharField(max_length=255)
    session_id = models.CharField(max_length=36, unique=True, default=uuid.uuid4)
    
    def __str__(self):
        return self.session_id
    
class Images(models.Model):
    image_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=255, blank=True) #fix later
    session_id = models.CharField(max_length=255)
    binary_encoding = models.BinaryField()

class Image_data(models.Model):
    face_data = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=255)
    session_id = models.CharField(max_length=255)
    focus_level = models.IntegerField()