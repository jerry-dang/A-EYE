from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import StudySessions
import uuid
from .serializers import SessionsSerializer

# Create your views here.
class StartSessionView(views.APIView):
    def post(self, request, format=None):
        serializer = SessionsSerializer(data=request.data)
        if serializer.is_valid():
            session_data = serializer.validated_data
            session_data['session_id'] = str(uuid.uuid4())
            session_object = StudySessions(**session_data)
            session_object.save()
            return Response(None, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)