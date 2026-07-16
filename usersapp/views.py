from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import SignUpserializer

from drf_yasg.utils import swagger_auto_schema 

# Create your views here.


class SignUpAPIView(APIView):
    @swagger_auto_schema(request_body=SignUpserializer)
    def post(self, request):
        serializer = SignUpserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
