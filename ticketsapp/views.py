from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response

from .models import OrderModel, TicketModel
from .serializers import OrderSerializer
from .services import create_order
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
