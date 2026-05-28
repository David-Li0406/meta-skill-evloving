# FastAPI Production Patterns - Quick Reference

## Database Lifecycle

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_async_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_recycle=3600,
    )
    app.state.db_engine = engine
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
```

## Partial Updates (PATCH)

```python
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

@app.patch("/users/{user_id}")
async def update_user(user_id: int, update: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    update_data = update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    await db.commit()
    return user
```

## Async Testing

```python
@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_endpoint(async_client: AsyncClient):
    response = await async_client.get("/users")
    assert response.status_code == 200
```

## Dependency Injection

```python
from functools import lru_cache

@lru_cache()
def get_settings():
    return Settings()

@app.get("/config")
async def get_config(settings: Settings = Depends(get_settings)):
    return settings.dict()
```

## File Uploads

```python
@app.post("/upload")
async def upload_file(file: UploadFile):
    # Stream the file
    df = pd.read_csv(file.file)
    return {"rows": len(df)}
```

## Background Tasks

```python
@app.post("/process")
async def start_process(background_tasks: BackgroundTasks):
    task_id = generate_task_id()
    background_tasks.add_task(long_running_task, task_id)
    return {"task_id": task_id}
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Engine at import time | Create in lifespan |
| Using `requests` | Use `httpx.AsyncClient` |
| Forgetting `exclude_unset=True` | Add it for PATCH |
| Sync TestClient | Use AsyncClient |
| Not disposing engine | Add `await engine.dispose()` |
