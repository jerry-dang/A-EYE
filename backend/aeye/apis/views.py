from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import StudySessions, Images, Image_data
from django.utils import timezone
import uuid
from .serializers import SessionsSerializer, ImagesSerializer, ImageDataSerializer
import base64 

# Create your views here.
class StartSessionView(views.APIView):
    def post(self, request, format=None):
        serializer = SessionsSerializer(data=request.data)
        if serializer.is_valid():
            session_data = serializer.validated_data
            session_data['session_id'] = str(uuid.uuid4())
            session_object = StudySessions(**session_data)
            session_object.save()
            return Response(session_data['session_id'], status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EndSessionView(views.APIView):
    def post(self, request, format=None):
        session_id = request.data.get('session_id')
        if not session_id:
            return Response({'error': 'session_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session_object = StudySessions.objects.get(session_id=session_id)
            session_object.end_time = timezone.now()  # Set end_time to the current time
            session_object.save()
            Images.objects.filter(session_id=session_id).delete()
            return Response(None, status=status.HTTP_200_OK)
        except StudySessions.DoesNotExist:
            return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
    #filter image by session id, delete all matching images 
class SaveImageView(views.APIView):
    def post(self, request, format=None):
        serializer = ImagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(self.request.data)
            return Response(None, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDataView(views.APIView):
    def get(self, request, format=None):
        # Extract query parameters
        session_id = request.query_params.get('session_id')
        user_id = request.query_params.get('user_id')
        
        # Validate query parameters
        if not session_id or not user_id:
            return Response({'error': 'Both session_id and user_id are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter the Image_data objects
        images = Image_data.objects.filter(session_id=session_id, user_id=user_id)
        
        # Serialize the data
        serializer = ImageDataSerializer(images, many=True)
        
        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)


