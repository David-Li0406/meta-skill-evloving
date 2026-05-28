# Exercise 03: FastAPI + PostgreSQL with Docker Compose

**Level**: Intermediate
**Time**: 30 minutes
**Goal**: Run a full-stack FastAPI application with a database

---

## Prerequisites

- Completed Exercises 01 and 02
- Basic FastAPI knowledge
- Docker running

---

## Part 1: Project Setup

### Step 1: Create Project Structure

```bash
mkdir fastapi-docker-compose
cd fastapi-docker-compose
```

Create this structure:
```
fastapi-docker-compose/
├── app/
│   └── main.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

### Step 2: Create FastAPI Application

Create `app/main.py`:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(title="Docker Learning API")

# Simple in-memory storage (we'll add DB later)
items = {}

class Item(BaseModel):
    name: str
    description: str | None = None

@app.get("/")
def root():
    return {
        "message": "Hello from FastAPI in Docker!",
        "environment": os.getenv("ENVIRONMENT", "unknown"),
        "database_url": os.getenv("DATABASE_URL", "not configured")[:20] + "..."
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in items:
        raise HTTPException(status_code=400, detail="Item exists")
    items[item_id] = item
    return {"item_id": item_id, **item.model_dump()}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, **items[item_id].model_dump()}

@app.get("/items")
def list_items():
    return {"items": items, "count": len(items)}
```

### Step 3: Create requirements.txt

```
fastapi[standard]>=0.109.0
uvicorn>=0.27.0
```

---

## Part 2: Simple Dockerfile

Create `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY ./app ./app

# Environment
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Run FastAPI
CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Part 3: First docker-compose.yml

Create `docker-compose.yml`:

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=docker
      - DATABASE_URL=not-connected-yet
```

### Step 1: Start the Service

```bash
docker compose up
```

**Expected Output**:
```
[+] Running 1/1
 ✔ Container fastapi-docker-compose-api-1  Created
Attaching to api-1
api-1  | INFO:     Started server process [1]
api-1  | INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Test the API

Open browser: http://localhost:8000

Or use curl:
```bash
curl http://localhost:8000
curl http://localhost:8000/health
curl http://localhost:8000/docs  # Swagger UI!
```

### Step 3: Stop

Press `Ctrl+C` or:
```bash
docker compose down
```

---

## Part 4: Add PostgreSQL Database

Update `docker-compose.yml`:

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=docker
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### Step 1: Start Both Services

```bash
docker compose up
```

**Watch the output**:
```
db-1   | PostgreSQL init process complete; ready for start up.
db-1   | LOG:  database system is ready to accept connections
api-1  | INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Test Database Connection

```bash
curl http://localhost:8000
```

You should see the DATABASE_URL is now configured!

---

## Part 5: Add Development Features

Update `docker-compose.yml` for hot-reload:

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app/app          # Mount code for live changes
    environment:
      - ENVIRONMENT=development
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app
    command: fastapi dev app/main.py --host 0.0.0.0 --port 8000
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: app
    ports:
      - "5432:5432"             # Expose for local tools
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### Step 1: Restart with New Config

```bash
docker compose down
docker compose up
```

### Step 2: Test Hot-Reload

1. Open http://localhost:8000
2. Edit `app/main.py` - change the message
3. Save the file
4. Refresh browser - see the change instantly!

---

## Part 6: Add Database Admin UI

Add Adminer for database management:

```yaml
services:
  api:
    # ... (same as before)

  db:
    # ... (same as before)

  adminer:
    image: adminer
    ports:
      - "8080:8080"
    depends_on:
      - db

volumes:
  postgres_data:
```

### Step 1: Start All Services

```bash
docker compose up
```

### Step 2: Access Adminer

1. Open http://localhost:8080
2. Login:
   - System: PostgreSQL
   - Server: db
   - Username: postgres
   - Password: postgres
   - Database: app
3. Explore the database!

---

## Part 7: Useful Commands

### View Logs

```bash
# All services
docker compose logs

# Follow logs
docker compose logs -f

# Specific service
docker compose logs -f api
```

### Run Commands in Container

```bash
# Open shell in API container
docker compose exec api bash

# Run Python in container
docker compose exec api python

# Connect to database
docker compose exec db psql -U postgres -d app
```

### Restart Services

```bash
# Restart API only
docker compose restart api

# Rebuild and restart
docker compose up --build
```

### Clean Up

```bash
# Stop and remove containers
docker compose down

# Also remove volumes (DATABASE DATA LOST!)
docker compose down -v
```

---

## Part 8: View Container Status

```bash
# See running containers
docker compose ps

# See resource usage
docker stats
```

---

## Challenges

### Challenge 1: Add Redis

Add a Redis service for caching:

```yaml
redis:
  image: redis:7-alpine
  ports:
    - "6379:6379"
```

### Challenge 2: Add Environment File

Create `.env`:
```
POSTGRES_PASSWORD=supersecret
```

Update compose to use it:
```yaml
db:
  environment:
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
```

### Challenge 3: Add Health Check to API

```yaml
api:
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
    interval: 30s
    timeout: 10s
    retries: 3
```

---

## Summary

| Concept | What You Learned |
|---------|------------------|
| docker-compose.yml | Define multi-container apps |
| services | Individual containers |
| depends_on | Service dependencies |
| healthcheck | Wait for services to be ready |
| volumes | Persist data & sync code |
| ports | Expose services |
| environment | Configure containers |

---

## What You Learned

1. **Docker Compose** simplifies multi-container apps
2. **Services** can depend on each other
3. **Health checks** ensure proper startup order
4. **Volumes** persist database data
5. **Bind mounts** enable hot-reload development
6. **One command** (`docker compose up`) starts everything

---

## Final docker-compose.yml

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app/app
    environment:
      - ENVIRONMENT=development
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app
    command: fastapi dev app/main.py --host 0.0.0.0 --port 8000
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: app
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  adminer:
    image: adminer
    ports:
      - "8080:8080"
    depends_on:
      - db

volumes:
  postgres_data:
```

---

## Next Exercise

Ready for Exercise 04? You'll create production-optimized multi-stage builds!
