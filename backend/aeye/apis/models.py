from django.db import models

# Create your models here.

class Sessions(models.Model):
    location = models.CharField()
    start_time = models.models.DateTimeField(auto_now_add=True)
    end_time = models.models.DateTimeField(auto_now=True)
    noise_level = models.CharField()
    session_id = models.CharField()
    
class Images(models.Model):
    image_id = models.CharField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField()
    session_id = models.CharField()
    binary_encoding = models.BinaryField()

class Image_data(models.Model):
    coordinates = models.CharField()
    expression = models.CharField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField()