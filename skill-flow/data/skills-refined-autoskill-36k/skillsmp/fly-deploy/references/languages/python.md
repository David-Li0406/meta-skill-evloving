# Python on fly.io

## FastAPI

### Dockerfile for FastAPI

See `assets/dockerfiles/fastapi.Dockerfile` for the complete template.

**Key points:**
- Use `python:3.11-slim` or `python:3.12-slim` base image
- Install dependencies with pip in virtual environment
- Use `uvicorn` as the ASGI server
- Run as non-root user
- Multi-stage build for minimal image size

### Basic FastAPI App Structure

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI(title="My API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        log_level="info"
    )
```

### fly.toml for FastAPI

```toml
app = "my-fastapi-app"
primary_region = "ord"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8080"
  PYTHONUNBUFFERED = "1"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = "stop"
  auto_start_machines = true
  min_machines_running = 0

  [[http_service.checks]]
    grace_period = "5s"
    interval = "30s"
    method = "GET"
    timeout = "5s"
    path = "/health"

[[vm]]
  memory = "256mb"
  cpus = 1
```

### Requirements Management

**requirements.txt:**
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
python-dotenv==1.0.0
```

**For production, pin all dependencies:**
```bash
pip freeze > requirements.txt
```

**Using Poetry:**
```toml
[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.109.0"
uvicorn = {extras = ["standard"], version = "^0.27.0"}
```

Dockerfile adjustment:
```dockerfile
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi
```

### Running with Uvicorn

**Development:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

**Production (in Dockerfile):**
```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

**With workers:**
```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]
```

**Using Gunicorn + Uvicorn workers (recommended for production):**

```dockerfile
RUN pip install gunicorn

CMD ["gunicorn", "main:app", \
     "--workers", "2", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8080"]
```

### Database Integration

**SQLAlchemy + PostgreSQL:**

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Fix for fly.io postgres URL (postgres:// -> postgresql://)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**requirements.txt additions:**
```txt
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
alembic==1.13.1
```

### Migrations with Alembic

**Initialize Alembic:**
```bash
alembic init alembic
```

**alembic.ini:**
```ini
sqlalchemy.url = ${DATABASE_URL}
```

**alembic/env.py:**
```python
import os
from sqlalchemy import engine_from_config, pool

config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))
```

**fly.toml release command:**
```toml
[deploy]
  release_command = "alembic upgrade head"
```

### Environment Variables

**Using python-dotenv:**
```python
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
```

**Set secrets:**
```bash
fly secrets set DATABASE_URL=postgresql://...
fly secrets set SECRET_KEY=$(openssl rand -hex 32)
```

### Static Files

**Serve static files:**
```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
```

**In Dockerfile:**
```dockerfile
COPY ./static /app/static
```

### Background Tasks

**FastAPI background tasks:**
```python
from fastapi import BackgroundTasks

def send_email(email: str):
    # Send email logic
    pass

@app.post("/send-notification")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email)
    return {"message": "Notification sent"}
```

**For longer tasks, consider:**
- Celery with Redis
- Fly.io Machines for one-off tasks
- External services (Upstash QStash, etc.)

### Logging

**Configure logging:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown")
```

View logs:
```bash
fly logs
```

### Common Issues

**Module not found:**
- Verify all dependencies in requirements.txt
- Check virtual environment activation in Dockerfile

**Database connection errors:**
- Ensure DATABASE_URL is set via `fly secrets`
- Check postgres:// vs postgresql:// prefix
- Verify database is attached: `fly postgres attach`

**Port binding issues:**
- Always bind to `0.0.0.0`, not `localhost` or `127.0.0.1`
- Use PORT environment variable from fly.io

**Slow cold starts:**
- Reduce image size with multi-stage builds
- Use `auto_stop_machines = "suspend"` instead of "stop"
- Keep min_machines_running = 1 for better response times

---

## Django

### Quick Django Setup

**Dockerfile:**
Similar to FastAPI but with Django-specific settings. Use `gunicorn` with `wsgi:application`.

**Key Django settings for fly.io:**

```python
# settings.py
import os
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = ['.fly.dev', 'yourdomain.com']

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Security
SECRET_KEY = os.getenv('SECRET_KEY')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

**fly.toml:**
```toml
[deploy]
  release_command = "python manage.py migrate && python manage.py collectstatic --noinput"

[[statics]]
  guest_path = "/app/staticfiles"
  url_prefix = "/static/"
```

---

## Flask

### Quick Flask Setup

**app.py:**
```python
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return {'message': 'Hello World'}

@app.route('/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 8080))
    )
```

**Run with Gunicorn:**
```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]
```

---

## Python Best Practices

### .dockerignore

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
.pytest_cache/
.git/
.env
*.db
*.sqlite3
```

### Virtual Environments in Docker

```dockerfile
# Create venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
```

### Multi-stage Build

```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Performance Monitoring

**Check memory usage:**
```bash
fly ssh console -C "free -m"
```

**Check Python process:**
```bash
fly ssh console -C "ps aux | grep python"
```

**Optimize memory:**
- Use `--workers 1` for small instances
- Monitor with `fly logs` for memory errors
- Scale up if needed: `fly scale memory 512`
