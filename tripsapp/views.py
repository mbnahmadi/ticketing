from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import TripsModel
from .serializers import TripsSerializer

from drf_yasg.utils import swagger_auto_schema 
# Create your views here.

class TripsListAPIView(APIView):
    # @swagger_auto_schema(request_body=TripsSerializer)
    def get(self, request):
        trips = TripsModel.objects.all()
        serializer = TripsSerializer(trips, many=True)

        return Response({"trips": serializer.data}, status=status.HTTP_200_OK)