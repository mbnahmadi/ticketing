from rest_framework import serializers
from .models import OrderModel, TicketModel
from tripsapp.models import TripsModel, TripSeatModel
from tripsapp.serializers import TripSeatSerializer, TripsSerializer,VehicleSerializer,TerminalSerializer,TerminalSerializer
from django.core.exceptions import ValidationError


class OrderSerializer(serializers.Serializer):
    trip = serializers.PrimaryKeyRelatedField(queryset=TripsModel.objects.all())
    trip_seats = serializers.PrimaryKeyRelatedField(queryset=TripSeatModel.objects.all(), many=True)

    def validate(self, attrs):
        trip = attrs["trip"]
        trip_seats = attrs["trip_seats"]

        if len(trip_seats) == 0:
            raise ValidationError({"trip_seats": "At least one seat must be selected."})
        if len(trip_seats) != len(set(seat.id for seat in trip_seats)):
            raise ValidationError({"you can select tripseat only one time."})

        for trip_seat in trip_seats:
            if trip_seat.trip != trip:
                raise ValidationError(
                    {
                        "trip_seats":
                        f"Seat {trip_seat.id} does not belong to this trip."
                    }
                )
            if trip_seat.status != TripSeatModel.TripSeatStatus.AVAILABLE:
                raise ValidationError(
                    {
                        "trip_seats":
                        f"Seat {trip_seat.seat.number} is not available."
                    }
                )

        return attrs




class TicketOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = ["order_number"]


class TicketTripsSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer()
    origin_terminal = TerminalSerializer()
    destination_terminal = TerminalSerializer()
    class Meta:
        model = TripsModel
        fields = ["id", "vehicle", "origin_terminal", "destination_terminal", "start_datetime"]

class TicketTripSeatSerializer(serializers.ModelSerializer):
    trip = TicketTripsSerializer()
    class Meta:
        model = TripSeatModel
        fields = ["trip", "seat"]

class TicketSerializer(serializers.ModelSerializer):
    trip_seat = TicketTripSeatSerializer()
    order = TicketOrderSerializer()
    class Meta:
        model = TicketModel
        fields = [ "order", "trip_seat", "price", "issued_at"]


class OrderTicketSerializer(serializers.ModelSerializer):
    trip_seat = TicketTripSeatSerializer()
    class Meta:
        model = TicketModel
        fields = ["price", "issued_at", "trip_seat"]

class OrderRetrieveSerializer(serializers.ModelSerializer):
    tickets = OrderTicketSerializer(many=True, read_only=True)

    class Meta:
        model = OrderModel
        fields = ["order_number" ,"issued_at" ,"final_price" ,"status", "tickets"]