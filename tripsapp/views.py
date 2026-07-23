from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response

from .models import TripsModel, TripSeatModel
from .serializers import TripsSerializer, TripSeatSerializer

from drf_yasg.utils import swagger_auto_schema 
# Create your views here.

# class TripsListAPIView(APIView):
#     # @swagger_auto_schema(request_body=TripsSerializer)
#     def get(self, request):
#         trips = TripsModel.objects.all()
#         serializer = TripsSerializer(trips, many=True)

#         return Response({"trips": serializer.data}, status=status.HTTP_200_OK)

class TripsListView(generics.ListAPIView):
    queryset = TripsModel.objects.all()
    serializer_class = TripsSerializer

class TtripView(generics.RetrieveAPIView):
    queryset = TripsModel.objects.all()
    serializer_class = TripsSerializer
    lookup_field = "pk"

# class TtripView(generics.ListAPIView):
#     serializer_class = TripsSerializer

#     def get_queryset(self):
#         queryset = TripsModel.objects.all()
#         pk = self.request.query_params.get("id")
#         if pk is not None:
#             queryset = TripsModel.filter(id=pk)
#         return queryset


    # lookup_field = "trip"
class TripSeatView(generics.ListAPIView):
    # queryset = TripSeatModel.objects.all()
    serializer_class = TripSeatSerializer

    def get_queryset(self):
        trip_id = self.kwargs.get("trip")
        return TripSeatModel.objects.filter(trip_id=trip_id).select_related('seat')