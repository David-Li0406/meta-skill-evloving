---
id: docker-compose
name: "Docker Compose"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# Docker Compose

## Overview

Docker Compose defines and runs multi-container Docker applications using YAML configuration. It simplifies development environments, testing, and single-host deployments by orchestrating services, networks, and volumes declaratively.

## When to Use

- Local development environments with multiple services
- Integration testing with real dependencies
- Single-host deployments (staging, small production)
- CI/CD pipeline testing environments
- Prototyping microservices architectures

## Key Concepts

| Concept | Description |
|---------|-------------|
| Service | Container configuration (image, ports, env, volumes) |
| Network | Communication channel between services |
| Volume | Persistent storage shared between containers |
| Profile | Group services for selective startup |
| Depends_on | Service startup order and health dependencies |
| Override | Environment-specific configuration layering |

## Implementation

### Production-Ready docker-compose.yml

```yaml
version: "3.9"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
      args:
        - VERSION=${VERSION:-latest}
    image: myapp:${VERSION:-latest}
    container_name: myapp
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://app:${DB_PASSWORD}@db:5432/appdb
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
      - LOG_LEVEL=${LOG_LEVEL:-info}
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
        reservations:
          cpus: "0.25"
          memory: 128M
    networks:
      - frontend
      - backend
    volumes:
      - app-data:/app/data
      - ./logs:/app/logs
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  db:
    image: postgres:16-alpine
    container_name: myapp-db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=app
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=appdb
      - PGDATA=/var/lib/postgresql/data/pgdata
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d appdb"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 256M

  redis:
    image: redis:7-alpine
    container_name: myapp-redis
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 100mb --maxmemory-policy allkeys-lru
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend
    deploy:
      resources:
        limits:
          cpus: "0.25"
          memory: 128M

  nginx:
    image: nginx:alpine
    container_name: myapp-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./certbot/conf:/etc/letsencrypt:ro
      - ./certbot/www:/var/www/certbot:ro
      - static-files:/var/www/static:ro
    depends_on:
      - app
    networks:
      - frontend
    healthcheck:
      test: ["CMD", "nginx", "-t"]
      interval: 30s
      timeout: 10s
      retries: 3

  worker:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    image: myapp:${VERSION:-latest}
    container_name: myapp-worker
    restart: unless-stopped
    command: celery -A app worker --loglevel=info --concurrency=2
    environment:
      - DATABASE_URL=postgres://app:${DB_PASSWORD}@db:5432/appdb
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - backend
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 256M
    profiles:
      - worker

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true

volumes:
  postgres-data:
  redis-data:
  app-data:
  static-files:
```

### Development Override (docker-compose.override.yml)

```yaml
version: "3.9"

services:
  app:
    build:
      target: development
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - DEBUG=true
      - LOG_LEVEL=debug
    command: npm run dev
    ports:
      - "8000:8000"
      - "9229:9229"  # Debug port

  db:
    ports:
      - "5432:5432"  # Expose for local tools

  redis:
    ports:
      - "6379:6379"  # Expose for local tools

  mailhog:
    image: mailhog/mailhog
    container_name: myapp-mailhog
    ports:
      - "1025:1025"
      - "8025:8025"
    networks:
      - backend
    profiles:
      - dev
```

### Production Override (docker-compose.prod.yml)

```yaml
version: "3.9"

services:
  app:
    image: registry.example.com/myapp:${VERSION}
    build: null  # Don't build in production
    restart: always
    deploy:
      mode: replicated
      replicas: 2
      resources:
        limits:
          cpus: "2.0"
          memory: 1G

  db:
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1G

  nginx:
    restart: always
```

### Environment File (.env.example)

```bash
# Application
VERSION=1.0.0
SECRET_KEY=change-me-in-production
LOG_LEVEL=info

# Database
DB_PASSWORD=secure-password-here

# External Services
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=noreply@example.com
SMTP_PASSWORD=smtp-password

# Feature Flags
ENABLE_FEATURE_X=false
```

### Common Commands

```bash
# Start all services
docker compose up -d

# Start with specific profile
docker compose --profile worker up -d

# Start with production config
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Build and start
docker compose up -d --build

# View logs
docker compose logs -f app

# Scale service
docker compose up -d --scale app=3

# Execute command in service
docker compose exec app python manage.py migrate

# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v

# Restart single service
docker compose restart app

# View service status
docker compose ps

# Pull latest images
docker compose pull
```

### Health Check Patterns

```yaml
# HTTP health check
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s

# TCP health check
healthcheck:
  test: ["CMD-SHELL", "nc -z localhost 8000"]
  interval: 30s
  timeout: 10s
  retries: 3

# Script health check
healthcheck:
  test: ["CMD", "/app/healthcheck.sh"]
  interval: 30s
  timeout: 10s
  retries: 3

# Database health check
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U $POSTGRES_USER -d $POSTGRES_DB"]
  interval: 10s
  timeout: 5s
  retries: 5
```

## Best Practices

1. **Use version 3.9+** - Latest compose specification with all features
2. **Define health checks** - Enable proper dependency ordering and monitoring
3. **Use depends_on with condition** - Wait for service health, not just start
4. **Separate networks** - Isolate frontend and backend networks
5. **Use named volumes** - Easier management and backup than bind mounts
6. **Set resource limits** - Prevent runaway containers from affecting host
7. **Use override files** - Separate dev/staging/prod configurations
8. **Never commit .env** - Use .env.example as template
9. **Configure logging** - Set rotation to prevent disk exhaustion
10. **Use profiles** - Group optional services for selective startup

## Common Pitfalls

1. **Hardcoded secrets** - Never put passwords in docker-compose.yml. Use environment variables or Docker secrets.

2. **Missing health checks** - depends_on without health condition only waits for container start, not service readiness.

3. **Using bind mounts in production** - Bind mounts tie containers to specific hosts. Use named volumes for data persistence.

4. **No resource limits** - Containers can consume all host resources. Always set memory and CPU limits.

5. **Exposed database ports** - Exposing database ports in production creates security risks. Only expose in development overrides.

6. **Missing restart policy** - Without restart policy, containers won't recover from crashes. Use `unless-stopped` or `always`.

## References

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Compose File Reference](https://docs.docker.com/compose/compose-file/)
- [Compose Profiles](https://docs.docker.com/compose/profiles/)
- [Networking in Compose](https://docs.docker.com/compose/networking/)
