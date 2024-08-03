from rest_framework import serializers
from .models import StudySessions

class SessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySessions
        fields = ['location', 'start_time', 'end_time', 'noise_level', 'session_id']
