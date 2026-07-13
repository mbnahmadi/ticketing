from django.contrib import admin
from .models import TripsModel, TerminalModel, VehicleModel, VehicleSectionModel, SeatModel, TripSeatModel
# Register your models here.

admin.site.register(TripsModel)
admin.site.register(TerminalModel)
admin.site.register(VehicleModel)
admin.site.register(VehicleSectionModel)
admin.site.register(SeatModel)
admin.site.register(TripSeatModel)