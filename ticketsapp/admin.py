from django.contrib import admin
from .models import TicketModel, OrderModel
# Register your models here.


admin.site.register(TicketModel)
admin.site.register(OrderModel)