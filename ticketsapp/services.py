from django.db import transaction

from .models import OrderModel, TicketModel
from tripsapp.models import TripSeatModel

from django.core.exceptions import ValidationError


@transaction.atomic
def create_order(*, user, trip, trip_seats):

    locked_tripseats = (TripSeatModel.objects
                        .select_for_update()
                        .filter(id__in=[seat.id for seat in trip_seats])
                        )

    for seat in locked_tripseats:
        if seat.status != TripSeatModel.TripSeatStatus.AVAILABLE:

            raise ValidationError(f"Seat number {seat.seat_number} is already reserved or inactive.")

    total_price = trip.price * len(trip_seats)

    order = OrderModel.objects.create(
        user=user,
        final_price=total_price,
        status=OrderModel.OrderStatus.PAID
    )


    tickets = []

    for trip_seat in trip_seats:

        ticket = TicketModel.objects.create(
            order=order,
            user=user,
            trip_seat=trip_seat,
            price=trip.price
        )

        tickets.append(ticket)

        trip_seat.status = TripSeatModel.TripSeatStatus.BOOKED
        trip_seat.save()


    return order