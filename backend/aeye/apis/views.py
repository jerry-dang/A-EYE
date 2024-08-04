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
import json
from collections import OrderedDict

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
            list_of_images_converted = []
            list_of_images = Images.objects.filter(session_id=session_id)
            #get_all_image(list_of_images, list_of_images_converted)
            #call algorithm 
            #here algorithm(list_of_images_converted)
            #call algorithm
            list_of_images.delete()
            return Response(None, status=status.HTTP_200_OK)
        except StudySessions.DoesNotExist:
            return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
    #filter image by session id, delete all matching images 
class SaveImageView(views.APIView):
    def post(self, request, format=None):
        # Extract data from the request
        user_id = request.data.get('user_id')
        session_id = request.data.get('session_id')
        base64_string = request.data.get('base64_string')
        
        # Validate that all required fields are present
        if not user_id or not session_id or not base64_string:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Decode the base64 string to binary
            binary_encoding = base64.b64decode(base64_string)
            
            # Generate a unique image ID
            image_id = str(uuid.uuid4())
            
            # Create and save the image record in the database
            image = Images(
                image_id=image_id,
                user_id=user_id,
                session_id=session_id,
                binary_encoding=binary_encoding
            )
            image.save()
            
            return Response({'message': 'Image saved successfully', 'image_id': image_id}, status=status.HTTP_201_CREATED)
        
        except (base64.binascii.Error, ValueError) as e:
            return Response({'error': 'Invalid base64 string'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ImageDataView(views.APIView):
    def get(self, request, format=None):
        # Extract query parameters
        session_id = request.data.get('session_id')
        user_id = request.data.get('user_id')
        
        # Validate query parameters
        if not session_id or not user_id:
            return Response({'error': 'Both session_id and user_id are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter the Image_data objects
        images = Image_data.objects.filter(session_id=session_id, user_id=user_id)
        
        # Serialize the data
        serializer = ImageDataSerializer(images, many=True)
        
        data = serializer.data
        # Return the serialized data
        #serializer.data
        return Response(data, status=status.HTTP_200_OK)


def get_all_image(list_image, new_list):
    for image in list_image:
        new_list.append(base64.b64encode(image.binary_encoding).decode('utf-8'))
    