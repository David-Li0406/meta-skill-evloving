"""Readers - read-only business logic.

Readers contain functions that retrieve and process data without side effects.
They should not modify database state or trigger external actions.

Example:

    def get_user_dashboard_data(user_id: int) -> dict:
        user = User.objects.get(id=user_id)
        return {
            "name": user.name,
            "recent_orders": list(user.orders.order_by("-created")[:5].values()),
        }
"""
