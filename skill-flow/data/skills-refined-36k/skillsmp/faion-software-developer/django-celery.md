# Celery Tasks Reference

## Task Definition

```python
from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task(
    name='orders.process_daily_report',
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(ConnectionError,),
)
def process_daily_report(self, category_id: int) -> dict:
    """Generate daily report for category."""
    from apps.catalog.models import Category

    try:
        category = Category.objects.get(pk=category_id)
        # Processing logic...
        return {'status': 'success', 'category': category.slug}
    except Category.DoesNotExist:
        logger.error(f"Category {category_id} not found")
        return {'status': 'error', 'reason': 'not_found'}
```

## Task Routing

```python
# config/celery.py
app.conf.task_routes = {
    'orders.*': {'queue': 'orders'},
    'emails.*': {'queue': 'emails'},
}
```

## Task Best Practices

**Idempotency:**
```python
@shared_task
def send_welcome_email(user_id: int) -> bool:
    user = User.objects.get(pk=user_id)

    # Check if already sent
    if user.welcome_email_sent:
        return False

    send_email(user.email, 'Welcome!')
    user.welcome_email_sent = True
    user.save(update_fields=['welcome_email_sent'])
    return True
```

**Retry with backoff:**
```python
@shared_task(
    bind=True,
    max_retries=5,
    autoretry_for=(requests.RequestException,),
    retry_backoff=True,
    retry_backoff_max=600,
)
def call_external_api(self, data: dict) -> dict:
    response = requests.post(API_URL, json=data, timeout=30)
    response.raise_for_status()
    return response.json()
```

**Timeouts:**
```python
@shared_task(
    soft_time_limit=300,  # 5 minutes
    time_limit=360,       # 6 minutes hard limit
)
def long_running_task():
    ...
```

## Calling Tasks

```python
# Async call
process_daily_report.delay(category_id=1)

# With countdown (delay in seconds)
send_welcome_email.apply_async(args=[user.id], countdown=60)

# With ETA
from datetime import datetime, timedelta
send_reminder.apply_async(
    args=[user.id],
    eta=datetime.now() + timedelta(hours=24)
)
```
