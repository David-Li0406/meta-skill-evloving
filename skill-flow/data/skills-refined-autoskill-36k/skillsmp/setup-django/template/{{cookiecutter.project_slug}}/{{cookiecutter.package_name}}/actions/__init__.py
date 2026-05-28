"""Actions - state-changing business logic.

Actions contain functions that modify state, either in the database or externally.
They encapsulate business rules and coordinate changes.

Example:

    def create_order(user_id: int, items: list[dict]) -> Order:
        user = User.objects.get(id=user_id)
        order = Order.objects.create(user=user, total=calculate_total(items))
        for item in items:
            OrderItem.objects.create(order=order, **item)
        send_order_confirmation_email(user, order)
        return order
"""
