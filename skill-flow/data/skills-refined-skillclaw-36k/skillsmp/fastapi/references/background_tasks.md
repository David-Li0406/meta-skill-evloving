# Background Tasks in FastAPI

Comprehensive guide for implementing background tasks and async job processing.

## Table of Contents

1. [FastAPI Background Tasks](#fastapi-background-tasks)
2. [Celery with Redis](#celery-with-redis)
3. [ARQ (Async Task Queue)](#arq-async-task-queue)
4. [Scheduled Tasks](#scheduled-tasks)
5. [Task Monitoring](#task-monitoring)

---

## FastAPI Background Tasks

Built-in background tasks for lightweight operations that don't need distributed processing.

### Basic Usage

```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def write_log(message: str):
    """Background task function."""
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")


@app.post("/send-notification/")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    return {"message": "Notification sent in the background"}
```

### Send Email in Background

```python
from fastapi import BackgroundTasks
import smtplib
from email.message import EmailMessage


def send_email(email: str, subject: str, body: str):
    """Send email in background."""
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = "noreply@example.com"
    msg['To'] = email

    with smtplib.SMTP('localhost', 1025) as server:
        server.send_message(msg)


@app.post("/register/")
async def register_user(email: str, background_tasks: BackgroundTasks):
    # Save user to database
    # ...

    # Send welcome email in background
    background_tasks.add_task(
        send_email,
        email,
        "Welcome!",
        "Thanks for registering!"
    )

    return {"message": "User registered", "email": email}
```

### Multiple Background Tasks

```python
@app.post("/order/")
async def create_order(order_id: int, background_tasks: BackgroundTasks):
    # Create order in database
    # ...

    # Add multiple background tasks
    background_tasks.add_task(send_confirmation_email, order_id)
    background_tasks.add_task(update_inventory, order_id)
    background_tasks.add_task(notify_warehouse, order_id)

    return {"message": "Order created", "order_id": order_id}
```

### With Dependencies

```python
from fastapi import Depends
from app.core.database import get_db


def process_data(db_session, data_id: int):
    """Background task with database session."""
    # Process data using db_session
    pass


@app.post("/process/")
async def trigger_processing(
    data_id: int,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    background_tasks.add_task(process_data, db, data_id)
    return {"message": "Processing started"}
```

### Limitations

- Tasks run in the same process
- Not suitable for long-running tasks
- No retry mechanism
- No task persistence
- Not distributed

**Use Cases:**
- Sending emails
- Logging
- Simple notifications
- Cache invalidation
- Non-critical updates

---

## Celery with Redis

For distributed, production-grade task processing.

### Installation

```bash
pip install celery redis
```

### Celery Configuration

```python
# app/core/celery_app.py
from celery import Celery

celery_app = Celery(
    "fastapi_celery",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
)
```

### Define Tasks

```python
# app/tasks/email_tasks.py
from app.core.celery_app import celery_app
import time


@celery_app.task(name="send_email_task")
def send_email_task(email: str, subject: str, body: str):
    """Celery task to send email."""
    time.sleep(2)  # Simulate email sending
    print(f"Email sent to {email}: {subject}")
    return {"status": "sent", "email": email}


@celery_app.task(name="process_large_file")
def process_large_file_task(file_path: str):
    """Process large file in background."""
    # Heavy processing logic
    time.sleep(10)
    return {"status": "processed", "file": file_path}


@celery_app.task(name="generate_report", bind=True)
def generate_report_task(self, user_id: int):
    """Generate report with progress tracking."""
    total = 100
    for i in range(total):
        time.sleep(0.1)
        # Update task state
        self.update_state(
            state="PROGRESS",
            meta={"current": i, "total": total}
        )
    return {"status": "completed", "user_id": user_id}
```

### Use Tasks in Endpoints

```python
# app/api/endpoints/tasks.py
from fastapi import APIRouter
from app.tasks.email_tasks import send_email_task, process_large_file_task

router = APIRouter()


@router.post("/send-email/")
async def send_email(email: str, subject: str, body: str):
    # Queue task
    task = send_email_task.delay(email, subject, body)

    return {
        "message": "Email queued",
        "task_id": task.id
    }


@router.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    from app.core.celery_app import celery_app

    task = celery_app.AsyncResult(task_id)

    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.ready() else None,
        "info": task.info  # Progress info for tasks that report it
    }


@router.post("/process-file/")
async def process_file(file_path: str):
    task = process_large_file_task.delay(file_path)

    return {
        "message": "File processing started",
        "task_id": task.id
    }
```

### Run Celery Worker

```bash
# Start Celery worker
celery -A app.core.celery_app worker --loglevel=info

# Start multiple workers
celery -A app.core.celery_app worker --loglevel=info --concurrency=4

# Start worker on Windows
celery -A app.core.celery_app worker --loglevel=info --pool=solo
```

### Docker Compose with Celery

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    depends_on:
      - redis
      - postgres

  celery_worker:
    build: .
    command: celery -A app.core.celery_app worker --loglevel=info
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    depends_on:
      - redis
      - postgres

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: dbname
```

### Task Retry

```python
@celery_app.task(
    name="send_email_with_retry",
    bind=True,
    max_retries=3,
    default_retry_delay=60  # Retry after 60 seconds
)
def send_email_with_retry(self, email: str):
    try:
        # Attempt to send email
        send_email(email)
    except Exception as exc:
        # Retry on failure
        raise self.retry(exc=exc)
```

---

## ARQ (Async Task Queue)

Modern async task queue for Python.

### Installation

```bash
pip install arq
```

### Configuration

```python
# app/core/arq_config.py
from arq import create_pool
from arq.connections import RedisSettings

REDIS_SETTINGS = RedisSettings(
    host='localhost',
    port=6379,
    database=0
)


async def get_arq_pool():
    return await create_pool(REDIS_SETTINGS)
```

### Define Tasks

```python
# app/tasks/arq_tasks.py
import asyncio


async def send_email_arq(ctx, email: str, subject: str, body: str):
    """ARQ task to send email."""
    await asyncio.sleep(2)  # Simulate async email sending
    print(f"Email sent to {email}: {subject}")
    return {"status": "sent", "email": email}


async def process_data_arq(ctx, data_id: int):
    """Process data asynchronously."""
    await asyncio.sleep(5)
    return {"status": "processed", "data_id": data_id}


# Worker configuration
class WorkerSettings:
    functions = [send_email_arq, process_data_arq]
    redis_settings = REDIS_SETTINGS
```

### Use in Endpoints

```python
from fastapi import APIRouter
from app.core.arq_config import get_arq_pool

router = APIRouter()


@router.post("/send-email-arq/")
async def send_email_endpoint(email: str, subject: str, body: str):
    pool = await get_arq_pool()

    job = await pool.enqueue_job(
        'send_email_arq',
        email,
        subject,
        body
    )

    return {
        "message": "Email queued",
        "job_id": job.job_id
    }


@router.get("/job-status/{job_id}")
async def get_job_status(job_id: str):
    pool = await get_arq_pool()
    job = Job(job_id, pool)

    status = await job.status()
    result = await job.result()

    return {
        "job_id": job_id,
        "status": status,
        "result": result
    }
```

### Run ARQ Worker

```bash
# Start ARQ worker
arq app.tasks.arq_tasks.WorkerSettings
```

---

## Scheduled Tasks

### APScheduler

```bash
pip install apscheduler
```

```python
# app/core/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


scheduler = AsyncIOScheduler()


async def cleanup_old_data():
    """Scheduled task to cleanup old data."""
    print("Cleaning up old data...")
    # Cleanup logic


async def send_daily_report():
    """Send daily report."""
    print("Sending daily report...")
    # Report generation and sending


def start_scheduler():
    # Run every day at midnight
    scheduler.add_job(
        cleanup_old_data,
        CronTrigger(hour=0, minute=0)
    )

    # Run every Monday at 9 AM
    scheduler.add_job(
        send_daily_report,
        CronTrigger(day_of_week='mon', hour=9, minute=0)
    )

    scheduler.start()
```

```python
# app/main.py
from fastapi import FastAPI
from app.core.scheduler import start_scheduler

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    start_scheduler()
```

### Celery Beat (Scheduled Celery Tasks)

```python
# app/core/celery_app.py
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    'cleanup-every-night': {
        'task': 'cleanup_old_data',
        'schedule': crontab(hour=0, minute=0),
    },
    'send-report-monday': {
        'task': 'send_weekly_report',
        'schedule': crontab(day_of_week=1, hour=9, minute=0),
    },
    'check-every-5-minutes': {
        'task': 'health_check',
        'schedule': 300.0,  # Every 5 minutes
    },
}
```

```bash
# Start Celery Beat
celery -A app.core.celery_app beat --loglevel=info

# Start worker and beat together
celery -A app.core.celery_app worker --beat --loglevel=info
```

---

## Task Monitoring

### Flower (Celery Monitoring)

```bash
# Install Flower
pip install flower

# Start Flower
celery -A app.core.celery_app flower --port=5555
```

Access at http://localhost:5555

### Docker Compose with Flower

```yaml
services:
  flower:
    image: mher/flower
    command: celery --broker=redis://redis:6379/0 flower --port=5555
    ports:
      - "5555:5555"
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    depends_on:
      - redis
```

---

## Best Practices

1. **Choose the right tool:**
   - FastAPI BackgroundTasks: Simple, quick tasks
   - Celery: Complex, distributed, production tasks
   - ARQ: Modern async task queue

2. **Handle failures gracefully** with retries
3. **Set timeouts** to prevent hanging tasks
4. **Monitor tasks** with Flower or similar tools
5. **Use task queues** to prevent blocking the main application
6. **Separate concerns** - keep tasks in separate modules
7. **Test tasks** independently from endpoints
8. **Log task execution** for debugging
9. **Use result backends** for task result retrieval
10. **Scale workers** independently from API servers

### Task Best Practices Example

```python
@celery_app.task(
    name="robust_task",
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    time_limit=300,  # 5 minutes hard limit
    soft_time_limit=240  # 4 minutes soft limit
)
def robust_task(self, data: dict):
    try:
        # Task logic
        result = process_data(data)
        return {"status": "success", "result": result}

    except SoftTimeLimitExceeded:
        # Handle soft timeout
        logger.warning("Task approaching time limit")
        cleanup()
        raise

    except Exception as exc:
        logger.error(f"Task failed: {exc}")
        # Retry on failure
        raise self.retry(exc=exc, countdown=60)
```
