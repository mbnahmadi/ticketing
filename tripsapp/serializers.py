from rest_framework import serializers
from .models import TripsModel, VehicleModel, TerminalModel, TripSeatModel, SeatModel

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = ["model"]

class TerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TerminalModel
        fields = ["name", "city_name"]

class TripsSerializer(serializers.ModelSerializer):
    available_seats = serializers.SerializerMethodField()
    vehicle = VehicleSerializer()
    origin_terminal = TerminalSerializer()
    destination_terminal = TerminalSerializer()
    class Meta:
        model = TripsModel
        fields = ["id", "vehicle", "origin_terminal", "destination_terminal", "start_datetime", "price", "available_seats"]

    def get_available_seats(self, obj):
        return obj.tripseatmodel_set.filter(status=TripSeatModel.TripSeatStatus.AVAILABLE).count
        # return obj.tripseatmodel_set.filter(status="A").count()


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatModel
        fields = ["number", "vehicle"]


class TripSeatSerializer(serializers.ModelSerializer):
    seat = SeatSerializer()
    # trip = TripsSerializer()
    class Meta:
        model = TripSeatModel
        fields = ["id", "seat", "status"]