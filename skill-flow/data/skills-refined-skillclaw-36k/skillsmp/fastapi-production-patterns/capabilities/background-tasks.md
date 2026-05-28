# Background Tasks

## Overview
Handling long-running operations in FastAPI using background tasks to avoid HTTP timeouts while providing status updates to users.

## Problem Statement
**Long operations kill HTTP:**
- HTTP requests timeout after 30-300 seconds
- Video processing, batch imports, report generation take minutes
- Users need status updates, not hanging connections
- Tasks may fail and need retry logic

## Patterns

### 1. FastAPI BackgroundTasks (Simple)

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Runs after response is sent
    time.sleep(2)  # Simulate email sending
    print(f"Email sent to {email}: {message}")

@app.post("/signup")
async def signup(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "Signup complete. Check your email."}
```

### 2. Task with Status Tracking

```python
from enum import Enum
import asyncio

class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

# In-memory task storage (use Redis/DB in production)
task_store: dict[str, dict] = {}

def long_running_task(task_id: str):
    try:
        task_store[task_id]["status"] = TaskStatus.PROCESSING

        # Do work
        result = process_heavy_computation()

        task_store[task_id]["status"] = TaskStatus.COMPLETED
        task_store[task_id]["result"] = result

    except Exception as e:
        task_store[task_id]["status"] = TaskStatus.FAILED
        task_store[task_id]["error"] = str(e)

@app.post("/process")
async def start_process(background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())

    task_store[task_id] = {
        "status": TaskStatus.PENDING,
        "created_at": datetime.now()
    }

    background_tasks.add_task(long_running_task, task_id)

    return {
        "task_id": task_id,
        "status": TaskStatus.PENDING,
        "message": "Task started"
    }

@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    if task_id not in task_store:
        raise HTTPException(status_code=404, detail="Task not found")

    return task_store[task_id]
```

### 3. Persistent Task Storage (Database)

```python
# models.py
class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True)
    status = Column(String, default="pending")
    result = Column(JSON, nullable=True)
    error = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

# Task function
async def process_task_async(task_id: str, db: AsyncSession):
    async with AsyncSession(engine) as session:
        try:
            # Update status
            task = await session.get(Task, task_id)
            task.status = "processing"
            await session.commit()

            # Do work
            result = await heavy_computation()

            # Update completion
            task.status = "completed"
            task.result = result
            task.completed_at = datetime.utcnow()
            await session.commit()

        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            await session.commit()
```

### 4. Celery for Production (Recommended)

```python
# celery_app.py
from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def process_video(video_id: str):
    # Long-running video processing
    result = video_processor.process(video_id)
    return {"video_id": video_id, "result": result}

# FastAPI integration
@app.post("/videos/{video_id}/process")
async def process_video_endpoint(video_id: str):
    task = process_video.delay(video_id)
    return {
        "task_id": task.id,
        "status": "processing"
    }

@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    result = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": result.state,
        "result": result.result if result.ready() else None
    }
```

## Comparison: BackgroundTasks vs Celery

| Feature | BackgroundTasks | Celery |
|---------|-----------------|--------|
| Setup complexity | Simple | Complex |
| Distributed execution | ❌ No | ✅ Yes |
| Task persistence | ❌ Lost on restart | ✅ Persistent |
| Retry logic | Manual | Built-in |
| Scheduling | ❌ No | ✅ Yes |
| Monitoring | ❌ No | ✅ Flower UI |
| Best for | Simple fire-and-forget | Production workloads |

## Error Handling

```python
def task_with_retry(task_id: str, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = do_work()
            return result
        except RetryableError as e:
            if attempt == max_retries - 1:
                # Final attempt failed
                task_store[task_id]["status"] = "failed"
                task_store[task_id]["error"] = str(e)
            else:
                # Retry with backoff
                time.sleep(2 ** attempt)
        except FatalError as e:
            # Don't retry fatal errors
            task_store[task_id]["status"] = "failed"
            task_store[task_id]["error"] = str(e)
            break
```

## Testing Background Tasks

```python
import pytest

@pytest.mark.asyncio
async def test_background_task():
    # Start task
    response = await client.post("/process")
    task_id = response.json()["task_id"]

    # Wait for completion
    await asyncio.sleep(2)

    # Check status
    response = await client.get(f"/tasks/{task_id}")
    assert response.json()["status"] == "completed"
```

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Not storing task results | Users can't get results | Use persistent storage |
| No error handling | Silent failures | Try/except with status updates |
| Using sync tasks | Blocks event loop | Use async/await |
| Losing tasks on restart | Data loss | Use Celery or DB persistence |
| No timeouts | Tasks hang forever | Add task timeouts |

## Production Checklist

- [ ] Use Celery for distributed execution
- [ ] Store task results in database/Redis
- [ ] Implement retry logic for transient failures
- [ ] Add task timeouts to prevent hanging
- [ ] Monitor task queue (Celery Flower)
- [ ] Set up task result expiration
- [ ] Handle worker crashes gracefully
- [ ] Log all task executions

## See Also
- [File Upload Handling](file-upload-handling.md)
- [Async Testing](async-testing.md)
