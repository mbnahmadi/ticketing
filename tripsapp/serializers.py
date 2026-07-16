from rest_framework import serializers
from .models import TripsModel, VehicleModel, TerminalModel

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = ["model"]

class TerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TerminalModel
        fields = "__all__"

class TripsSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer()
    origin_terminal = TerminalSerializer()
    destination_terminal = TerminalSerializer()
    class Meta:
        model = TripsModel
        fields = "__all__"
