from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import User, Order, Ticket

@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> None:

    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
    order.save()

    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"]
        )

def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user=get_user_model().objects.get(username=username))

    return Order.objects.all()
