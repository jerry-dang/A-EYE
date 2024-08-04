from django.db import models
import uuid

# Create your models here.

class StudySessions(models.Model):
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    noise_level = models.CharField(max_length=255)
    
    
class Images(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.ForeignKey(StudySessions, null=True, on_delete=models.SET_NULL)
    b64_encoding = models.TextField(null=True, blank=True)

class Image_data(models.Model):
    face_data = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.ForeignKey(StudySessions, null=True, on_delete=models.SET_NULL)
    focus_level = models.IntegerField()