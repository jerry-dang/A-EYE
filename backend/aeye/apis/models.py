from django.db import models

# Create your models here.

class StudySessions(models.Model):
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    noise_level = models.CharField(max_length=255)
    session_id = models.CharField(max_length=255)
    
class Images(models.Model):
    image_id = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=255)
    session_id = models.CharField(max_length=255)
    binary_encoding = models.BinaryField(max_length=255)

class Image_data(models.Model):
    face_data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=255)
    session_id = models.CharField(max_length=255)