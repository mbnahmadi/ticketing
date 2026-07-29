from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.contrib.auth import get_user_model

from .serializers import SignUpserializer

from drf_yasg.utils import swagger_auto_schema 

# Create your views here.

User = get_user_model()

class SignUpAPIView(APIView):
    
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=SignUpserializer)
    def post(self, request):
        serializer = SignUpserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class SignUpAPIView(generics.CreateAPIView):
#     query_set = User.objects.all()
#     serializer_class = SignUpserializer
#     permission_class = [AllowAny]