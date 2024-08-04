import uuid
import base64 

from .image_processing.image_processing import DataAggregator
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
from .serializers import SessionsSerializer, ImagesSerializer, ImageDataSerializer
from collections import OrderedDict

# Create your views here.
class StartSessionView(views.APIView):
    def post(self, request, format=None):
        serializer = SessionsSerializer(data=request.data)
        if serializer.is_valid():
            session_data = serializer.validated_data
            session_object = StudySessions(**session_data)
            session_object.save()
            return Response(session_object.id, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EndSessionView(views.APIView):
    def post(self, request, format=None):
        session_id = request.data.get('session_id')
        if not session_id:
            return Response({'error': 'session_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session_object = StudySessions.objects.get(id=session_id)
            session_object.end_time = timezone.now()  # Set end_time to the current time
            session_object.save()
            list_of_images = Images.objects.filter(session_id=session_id)
            print(list_of_images)
            base64_images = []
            for image in list_of_images:
                # base64_encoded = base64.b64encode(image.binary_encoding).decode('utf-8')
                base64_images.append({
                    'timestamp': image.timestamp,
                    'base64_encoded': image.b64_encoding
                })
            # print(base64_images)
            #get_all_image(list_of_images, list_of_images_converted)
            #call algorithm 
            print("==== I WAS HERE === ")
            # print(base64_images)
            dataAggregator = DataAggregator(base64_images)
            res = dataAggregator.process_images()
            print(res)

            #here algorithm(list_of_images_converted)
            #call algorithm
            # list_of_images.delete() TODO: bring back in production
            
            # save the data points
            for data in res:
                image_data = Image_data(
                    face_data=str(data["face_data"]),
                    timestamp=data["timestamp"],
                    session_id=session_object,
                    focus_level=data["focus"]
                )
                image_data.save()
            return Response(None, status=status.HTTP_200_OK)
        except StudySessions.DoesNotExist:
            return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
    #filter image by session id, delete all matching images 
class SaveImageView(views.APIView):
    def post(self, request, format=None):
        # Extract data from the request
        session_id = request.data.get('session_id')
        base64_string = request.data.get('base64_string')
        
        # Validate that all required fields are present
        if not session_id or not base64_string:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
        # print(base64_string)
        try:
            # Decode the base64 string to binary
            
            # Generate a unique image ID
            
            # Create and save the image record in the database
            study_session = StudySessions.objects.get(id=session_id)
            image = Images(
                session_id=study_session,
                b64_encoding=base64_string
            )
            image.save()
        
            return Response({'message': 'Image saved successfully', 'image_id': image.id}, status=status.HTTP_201_CREATED)
        
        except (base64.binascii.Error, ValueError) as e:
            print(e)
            return Response({'error': 'Invalid base64 string'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ImageDataView(views.APIView):
    def get(self, request, format=None):
        # Extract query parameters
        session_id = request.data.get('session_id')
        
        # Validate query parameters
        if not session_id:
            return Response({'error': 'Both session_id are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter the Image_data objects
        images = Image_data.objects.filter(session_id=session_id)
        
        # Serialize the data
        serializer = ImageDataSerializer(images, many=True)
        
        data = serializer.data
        # Return the serialized data
        #serializer.data
        return Response(data, status=status.HTTP_200_OK)


def get_all_image(list_image, new_list):
    for image in list_image:
        obj = {}
        converted_string = base64.b64encode(image.binary_encoding).decode('utf-8')
        obj["base64_encoded"] = converted_string
        obj["timestamp"] = image.timestamp
        new_list.append(obj)
        
    