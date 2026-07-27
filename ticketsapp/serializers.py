from rest_framework import serializers
from .models import OrderModel
from tripsapp.models import TripsModel, TripSeatModel
from django.core.exceptions import ValidationError


class OrderSerializer(serializers.Serializer):
    trip = serializers.PrimaryKeyRelatedField(queryset=TripsModel.objects.all())
    trip_seats = serializers.PrimaryKeyRelatedField(queryset=TripSeatModel.objects.all(), many=True)

    def validate(self, attrs):
        trip = attrs["trip"]
        trip_seats = attrs["trip_seats"]

        if len(trip_seats) == 0:
            raise ValidationError({"trip_seats": "At least one seat must be selected."})
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

        