from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

# Create your models here.


class TripsModel(models.Model):
    vehicle = models.ForeignKey("VehicleModel", on_delete=models.CASCADE)
    origin_terminal = models.ForeignKey("TerminalModel", on_delete=models.CASCADE, related_name="triporigin")
    destination_terminal = models.ForeignKey("TerminalModel", on_delete=models.CASCADE, related_name="tripdestination")

    start_datetime = models.DateTimeField(null=False, blank=False)
    # end_datetime = models.DateTimeField()

    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=False, blank=False)

    def clean(self):
        if self.origin_terminal == self.destination_terminal:
            raise ValidationError(
                {"destination_terminal": "origin and destination can not be same."}
            )
        # if self.end_datetime < self.start_datetime:
        #     raise ValidationError(
        #         {"end_datetime": "the end time must be after the start time."}
        #     )
            
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.origin_terminal} to {self.destination_terminal} - on {self.start_datetime}"


class TerminalModel(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    city_name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.name} in {self.city_name}"



class VehicleModel(models.Model):
    class VehicleTypeStatus(models.TextChoices):
        TRAIN = "t", "Train"
        PLANE = "a", "Airplane"
        BUS = "b", "bus"
    model = models.CharField(max_length=200, null=False, blank=False)
    capacity = models.PositiveIntegerField(null=False, blank=False)
    type = models.CharField(max_length=20, choices=VehicleTypeStatus.choices, null=False, blank=False)

    def __str__(self):
        return f"{self.type} - {self.model}"



class VehicleSectionModel(models.Model):
    row = models.CharField(max_length=100)
    vehicle = models.ForeignKey("VehicleModel", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row", "vehicle"],
                name = "unique_row_per_vehicle"
            )
        ]
    
    def __str__(self):
        return f"{self.vehicle.type} - {self.vehicle.model} - {self.row}"


class SeatModel(models.Model):
    number = models.PositiveIntegerField()
    vehicle = models.ForeignKey("VehicleModel", on_delete=models.CASCADE, related_name="seats")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["vehicle", "number"],
                name = "unique_seat_number_per_vehicle"
            )
        ]

    def clean(self):
        super().clean()
        if self.pk is None:
            if self.vehicle.seats.count() >= self.vehicle.capacity:
                raise ValidationError({"number": "The number of seats created exceeds the vehicle's capacity."})


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)    

    def __str__(self):
        return f"{self.number} from {self.vehicle.type} - {self.vehicle.model}"


class TripSeatModel(models.Model):
    class TripSeatStatus(models.TextChoices):
        AVAILABLE = "A", "available"
        # RESERVED = "r", "reserved"
        BOOKED = "b", "booked"
    trip = models.ForeignKey("TripsModel", on_delete=models.CASCADE)
    seat = models.ForeignKey("SeatModel", on_delete=models.CASCADE)
    status = models.CharField(choices=TripSeatStatus.choices, default=TripSeatStatus.AVAILABLE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["trip", "seat"],
                name= "unique_seat_number_per_trip"
            )
        ]

    def __str__(self):
        return f"{self.trip.origin_terminal} to {self.trip.destination_terminal} - {self.seat.vehicle.type} - {self.seat.number} is {self.status}"