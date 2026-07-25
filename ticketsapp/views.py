from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response

from .models import TripsModel, TripSeatModel
from .serializers import OrderSerializer
# Create your views here.

class OrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    def get_queryset(self):
        trip = self.request.query_params.get("trip")
        tripseat = self.request.query_params.get("tripseat")
