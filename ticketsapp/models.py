from django.db import models
from django.contrib.auth import get_user_model
from tripsapp.models import TripsModel,SeatModel, TripSeatModel

# Create your models here.

User = get_user_model()

class TicketModel(models.Model):
    order = models.ForeignKey("OrderModel",on_delete=models.CASCADE,related_name="tickets")
    # trip = models.ForeignKey(TripsModel,on_delete=models.CASCADE,related_name="tickets")
    # seat = models.ForeignKey(SeatModel,on_delete=models.CASCADE,related_name="tickets")
    trip_seat = models.ForeignKey(TripSeatModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="tickets")
    price = models.DecimalField(max_digits=10,decimal_places=2)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.trip_seat.seat.number}"


class OrderModel(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        CANCELED = "canceled", "Canceled"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=30, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    def __str__(self):
        return self.order_number