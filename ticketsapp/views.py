from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import OrderModel, TicketModel
from .serializers import OrderSerializer, TicketSerializer, OrderRetrieveSerializer
from .services import create_order

from django.db.models import Prefetch

# Create your views here.

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer


    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        order = create_order(
            user=request.user,
            trip=serializer.validated_data["trip"],
            trip_seats=serializer.validated_data["trip_seats"]
        )


        return Response(
            {
                "order_number": order.order_number
            },
            status=status.HTTP_201_CREATED
        )

class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    def get_queryset(self):
        return TicketModel.objects.filter(user=self.request.user).select_related(
            "order",
            "trip_seat",
            "trip_seat__trip",
            "trip_seat__seat",
            "trip_seat__trip__vehicle"
        )

class TicketRetrieveView(generics.RetrieveAPIView):
    serializer_class = TicketSerializer
    lookup_field = "id"
    def get_queryset(self):
        return TicketModel.objects.filter(user=self.request.user).select_related(
            "order",
            "trip_seat",
            "trip_seat__trip",
            "trip_seat__seat",
            "trip_seat__trip__vehicle"
        )


class OrderRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = OrderModel.objects.all()
    serializer_class = OrderRetrieveSerializer
    lookup_field = "order_number"
    def get_queryset(self):
        return OrderModel.objects.prefetch_related(
            Prefetch("tickets", 
            queryset = TicketModel.objects.select_related(
                "trip_seat",
                "trip_seat__seat",
                "trip_seat__trip",
                "trip_seat__trip__vehicle",
                "trip_seat__trip__origin_terminal",
                "trip_seat__trip__destination_terminal",
            ),
            )).filter(user=self.request.user)