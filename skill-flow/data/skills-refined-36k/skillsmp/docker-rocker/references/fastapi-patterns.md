# FastAPI Docker Patterns

Docker configurations specific to FastAPI, Pydantic, SQLModel, and async Python applications.

---

## FastAPI Server Configuration

### Development vs Production

```dockerfile
# Development (with hot-reload)
CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]

# Production (optimized)
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]

# Production with multiple workers
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4", "--proxy-headers"]
```

### Exec Form Required

```dockerfile
# CORRECT: Exec form (array) - receives signals properly
CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# WRONG: Shell form - breaks signal handling
CMD fastapi run app/main.py --port 80
```

### Proxy Headers

When running behind a reverse proxy (Nginx, Traefik, load balancer):

```dockerfile
# Enable proxy header forwarding
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
```

This ensures:
- Correct client IP in logs
- Proper HTTPS detection
- Accurate host headers

---

## Pydantic Settings in Containers

### Environment-Based Configuration

```python
# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Database
    database_url: str

    # Server
    port: int = 80
    workers: int = 1

    # Security
    secret_key: str
    allowed_hosts: list[str] = ["*"]

    # Environment
    environment: str = "production"
    debug: bool = False

settings = Settings()
```

### Docker Environment Variables

```dockerfile
# Set defaults, override at runtime
ENV DATABASE_URL="" \
    PORT=80 \
    WORKERS=1 \
    ENVIRONMENT=production \
    DEBUG=false
```

### docker-compose Environment

```yaml
services:
  api:
    build: .
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/app
      - SECRET_KEY=${SECRET_KEY}
      - ENVIRONMENT=production
    env_file:
      - .env.production
```

---

## SQLModel/Database Connections

### Async Engine for Containers

```python
# app/core/database.py
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings

# NullPool for external connection pooling (Neon, PgBouncer)
engine = create_async_engine(
    settings.database_url,
    poolclass=NullPool,
    pool_pre_ping=True,
    echo=settings.debug,
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
```

### Why NullPool?

| Scenario | Pool Type | Reason |
|----------|-----------|--------|
| Neon PostgreSQL | NullPool | Neon has built-in PgBouncer |
| PgBouncer | NullPool | External pooler manages connections |
| Direct PostgreSQL | QueuePool | Local pooling beneficial |
| Serverless/Lambda | NullPool | Connections don't persist |

### Connection String Formats

```python
# Neon PostgreSQL (pooled endpoint)
DATABASE_URL=postgresql+asyncpg://user:pass@ep-xxx.neon.tech/db?sslmode=require

# Neon (direct - for migrations only)
DATABASE_URL_DIRECT=postgresql+asyncpg://user:pass@ep-xxx.neon.tech/db?sslmode=require&options=endpoint%3Dep-xxx

# Local PostgreSQL
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/db
```

---

## Health Checks

### FastAPI Health Endpoint

```python
# app/routers/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.database import get_session

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.get("/health/db")
async def db_health_check(session: AsyncSession = Depends(get_session)):
    try:
        await session.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}
```

### Dockerfile Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:80/health')" || exit 1
```

### docker-compose Health Check

```yaml
services:
  api:
    build: .
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:80/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
```

---

## Lifespan Events

### Startup/Shutdown in Containers

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables, warm caches
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.create_all)
        pass

    yield

    # Shutdown: close connections
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
```

### Graceful Shutdown

The exec form `CMD ["fastapi", ...]` ensures:
- SIGTERM is received by the process
- Lifespan shutdown runs
- Connections close gracefully

```yaml
# docker-compose.yml
services:
  api:
    stop_grace_period: 30s  # Time for graceful shutdown
```

---

## Testing Configuration

### Test Dockerfile Stage

```dockerfile
FROM builder AS testing

# Install dev dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

COPY . .

# Override for test database
ENV DATABASE_URL=sqlite+aiosqlite:///./test.db \
    ENVIRONMENT=testing

CMD ["pytest", "-v", "--cov=app"]
```

### pytest with Docker

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

from app.main import app
from app.core.database import get_session

# Test database
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture
async def session():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        yield session

    await engine.dispose()

@pytest.fixture
async def client(session):
    async def override_session():
        yield session

    app.dependency_overrides[get_session] = override_session

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
```

---

## Worker Configuration

### CPU-Based Workers

```dockerfile
# Auto-detect CPU count
CMD ["sh", "-c", "fastapi run app/main.py --port 80 --workers $(nproc)"]

# Or use Gunicorn for more control
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:80"]
```

### Worker Recommendations

| Deployment | Workers | Memory per Worker |
|------------|---------|-------------------|
| Kubernetes pod | 1 | 256-512MB |
| Single container | CPU cores | 256MB each |
| Development | 1 | 512MB |

### Memory Considerations

```yaml
# docker-compose.yml
services:
  api:
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
    environment:
      - WORKERS=4  # 4 workers × 256MB = 1GB limit
```

---

## Common Patterns

### API Behind Reverse Proxy

```yaml
# docker-compose.yml
services:
  api:
    build: .
    expose:
      - "80"  # Internal only
    environment:
      - ROOT_PATH=/api/v1
    command: ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

```python
# app/main.py
from app.core.config import settings

app = FastAPI(root_path=settings.root_path)
```

### Migrations in Containers

```yaml
# docker-compose.yml
services:
  migrate:
    build: .
    command: ["alembic", "upgrade", "head"]
    environment:
      # Use direct connection for migrations
      - DATABASE_URL=${DATABASE_URL_DIRECT}
    depends_on:
      db:
        condition: service_healthy
```

**Important**: Use direct (non-pooled) connection for Alembic migrations with Neon/PgBouncer.
