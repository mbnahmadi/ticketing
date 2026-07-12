from django.db import models

# Create your models here.


class TripsModel(models.Model):
    origin_teminall = models.ForeignKey()
    destination_terminal = models.ForeignKey()

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    price = models.DecimalField(max_digits=10, decimal_places=2)