from rest_framework import serializers
from .models import OrderModel
from tripsapp.models import TripsModel, TripSeatModel
from django.core.exceptions import ValidationError


class OrderSerializer(serializers.ModelSerializer):
    trip = serializers.CharField()
    tripseat = serializers.CharField()
    class Meta:
        model = OrderModel
        fields = "__all__"

    def validate(self, attr):
        trip_exist = TripsModel.objects.get(id=attr["trip"]).exists()
        tripseat_exist = TripSeatModel.objects.get(id=attr["tripseat"]).exists()
        if not trip_exist:
            ValidationError({"trip": "trip does not exist."})

        if not tripseat_exist:
            ValidationError({"tripseat": "seat does not exist."})
        
        return attr

        