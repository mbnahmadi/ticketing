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
    available_seat = serializers.SerializerMethodField()
    vehicle = VehicleSerializer()
    origin_terminal = TerminalSerializer()
    destination_terminal = TerminalSerializer()
    class Meta:
        model = TripsModel
        fields = ["vehicle", "origin_terminal", "destination_terminal", "start_datetime", "price", "available_seat"]

    def get_available_seat(self, obj):
        return obj.tripseatmodel_set.filter(status="A").count()


class SeatSerializer(serializers.ModelSerializer):
    model = SeatModel
    fields = ["number", "vehicle"]


class TripSeatSerializer(serializers.ModelSerializer):
    # seat = SeatSerializer()
    # trip = TripsSerializer()
    class Meta:
        model = TripSeatModel
        fields = ["id", "seat", "status"]