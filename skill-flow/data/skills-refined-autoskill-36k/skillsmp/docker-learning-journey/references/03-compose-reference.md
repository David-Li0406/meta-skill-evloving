# Docker Compose Reference

Run multi-container applications with a single command.

---

## What is Docker Compose?

**Problem**: Running multiple containers manually is tedious:

```bash
# Create network
docker network create myapp

# Start database
docker run -d --name db --network myapp \
  -e POSTGRES_PASSWORD=secret postgres:15

# Start app
docker run -d --name api --network myapp \
  -p 8000:8000 -e DATABASE_URL=... myapp:latest
```

**Solution**: Docker Compose = One file, one command

```yaml
# docker-compose.yml
services:
  api:
    build: .
    ports:
      - "8000:8000"
  db:
    image: postgres:15
```

```bash
docker compose up  # That's it!
```

---

## docker-compose.yml Structure

```yaml
# Version is now optional (Compose V2)

services:           # Define your containers
  service-name:
    # Configuration here

volumes:            # Persistent data storage
  volume-name:

networks:           # Custom networks
  network-name:
```

---

## Services Configuration

### Build from Dockerfile

```yaml
services:
  api:
    build: .                    # Build from ./Dockerfile

  api-custom:
    build:
      context: .                # Build context
      dockerfile: Dockerfile.dev # Custom Dockerfile name
      target: development       # Multi-stage target
      args:
        PYTHON_VERSION: "3.12"  # Build arguments
```

### Use Existing Image

```yaml
services:
  db:
    image: postgres:15-alpine

  redis:
    image: redis:7
```

### Port Mapping

```yaml
services:
  api:
    ports:
      - "8000:8000"     # host:container
      - "8001:8000"     # Different host port

  api-internal:
    expose:
      - "8000"          # Internal only (no host mapping)
```

### Environment Variables

```yaml
services:
  api:
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
      - DEBUG=true

  # Or from file
  api-from-file:
    env_file:
      - .env
      - .env.local
```

### Volumes

```yaml
services:
  api:
    volumes:
      # Named volume (persistent)
      - app_data:/app/data

      # Bind mount (development - live code sync)
      - ./app:/app/app

      # Anonymous volume (exclude from bind mount)
      - /app/.venv

volumes:
  app_data:           # Declare named volume
```

### Dependencies

```yaml
services:
  api:
    depends_on:
      - db              # Simple dependency

  api-with-health:
    depends_on:
      db:
        condition: service_healthy  # Wait for health check
```

### Health Checks

```yaml
services:
  db:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
      start_period: 10s
```

### Restart Policy

```yaml
services:
  api:
    restart: unless-stopped

    # Options:
    # "no" - Never restart
    # "always" - Always restart
    # "on-failure" - Restart on error exit
    # "unless-stopped" - Always, unless manually stopped
```

### Resource Limits

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

---

## Complete FastAPI + PostgreSQL Example

```yaml
# docker-compose.yml

services:
  # FastAPI Application
  api:
    build:
      context: .
      target: development        # Use dev stage for hot-reload
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app/app          # Live code sync
      - /app/.venv              # Exclude venv
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/app
      - DEBUG=true
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  # PostgreSQL Database
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
    restart: unless-stopped

  # Database Admin UI (optional)
  adminer:
    image: adminer
    ports:
      - "8080:8080"
    depends_on:
      - db
    profiles:
      - admin                   # Only start with --profile admin

volumes:
  postgres_data:
```

---

## Commands Reference

### Start Services

```bash
# Start all services
docker compose up

# Start in background
docker compose up -d

# Start specific service
docker compose up api

# Start with rebuild
docker compose up --build

# Start with specific profile
docker compose --profile admin up
```

### Stop Services

```bash
# Stop (keep containers)
docker compose stop

# Stop and remove containers
docker compose down

# Stop and remove everything (including volumes)
docker compose down -v
```

### View Status

```bash
# List running services
docker compose ps

# View logs
docker compose logs

# Follow logs
docker compose logs -f

# Logs for specific service
docker compose logs -f api
```

### Execute Commands

```bash
# Run command in service
docker compose exec api bash

# Run one-off command
docker compose run --rm api pytest

# View service output
docker compose logs api
```

### Build & Update

```bash
# Build images
docker compose build

# Build specific service
docker compose build api

# Pull latest images
docker compose pull

# Recreate containers
docker compose up -d --force-recreate
```

---

## Networks

### Default Network

Compose creates a default network. Services can reach each other by service name:

```yaml
services:
  api:
    # Can connect to "db" by hostname
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
  db:
    image: postgres:15
```

### Custom Networks

```yaml
services:
  api:
    networks:
      - frontend
      - backend

  db:
    networks:
      - backend          # Only on backend network

networks:
  frontend:
  backend:
    internal: true       # No external access
```

---

## Volumes Explained

### Named Volumes (Persistent Data)

```yaml
services:
  db:
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:         # Data survives container restart
```

### Bind Mounts (Development)

```yaml
services:
  api:
    volumes:
      - ./app:/app/app   # Sync local files into container
      # Changes on host → Immediately in container
      # Perfect for development!
```

### Exclude from Bind Mount

```yaml
services:
  api:
    volumes:
      - .:/app           # Mount everything
      - /app/.venv       # EXCEPT .venv (anonymous volume)
      - /app/__pycache__ # EXCEPT cache
```

---

## Profiles (Optional Services)

```yaml
services:
  api:
    # Always starts

  adminer:
    profiles:
      - debug            # Only with --profile debug

  test:
    profiles:
      - testing          # Only with --profile testing
```

```bash
# Start without optional services
docker compose up

# Start with debug services
docker compose --profile debug up

# Start with multiple profiles
docker compose --profile debug --profile testing up
```

---

## Environment Files

### .env (Auto-loaded)

```bash
# .env (in same directory as docker-compose.yml)
POSTGRES_PASSWORD=secretpassword
APP_DEBUG=true
```

```yaml
services:
  db:
    environment:
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
```

### Multiple Environment Files

```yaml
services:
  api:
    env_file:
      - .env
      - .env.local      # Overrides .env
```

---

## Multiple Compose Files

### Override for Development

```yaml
# docker-compose.yml (base)
services:
  api:
    build: .

# docker-compose.override.yml (auto-merged in dev)
services:
  api:
    volumes:
      - ./app:/app/app
    environment:
      - DEBUG=true
```

### Override for Production

```bash
# Use specific override file
docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```

---

## Common Patterns

### Wait for Database

```yaml
services:
  api:
    depends_on:
      db:
        condition: service_healthy

  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 5s
      retries: 5
```

### Development Hot-Reload

```yaml
services:
  api:
    build:
      target: development
    volumes:
      - ./app:/app/app
    command: fastapi dev app/main.py --host 0.0.0.0
```

### Run Migrations

```yaml
services:
  migrate:
    build: .
    command: alembic upgrade head
    depends_on:
      db:
        condition: service_healthy
    profiles:
      - migrate
```

```bash
docker compose --profile migrate up migrate
```
