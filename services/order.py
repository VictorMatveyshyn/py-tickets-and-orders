from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import User, Order, Ticket

@transaction.atomic
def create_order(tickets: list[dict]) -> None:
    for ticket in tickets:
        user = get_user_model().objects.get(username=ticket["username"])
        order = Order.objects.create(uswer=user)
        date = ticket.get("created_at", None)
        if date:
            order.created_at = date
        order.save()
        Ticket.objects.create(
            order=order,
            movie_session=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"]
        )

def get_orders(username: str = None) -> QuerySet(Order):
    if username:
        return Order.objects.filter(user=get_user_model().objects.get(username=username))

    return Order.objects.all()
