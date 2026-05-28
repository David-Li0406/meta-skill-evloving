---
name: docker-containers
description: "Docker containerization best practices. Use when building Docker images, writing Dockerfiles, configuring Docker Compose, or troubleshooting container issues."
---

# Docker Containerization

Comprehensive guide for building, optimizing, and deploying containerized applications with Docker.

## When to Use

- Building Docker images for applications
- Writing and optimizing Dockerfiles
- Setting up Docker Compose for local development
- Debugging container issues
- Securing container deployments
- Multi-stage builds for production

## Core Concepts

### Dockerfile Best Practices

**Multi-Stage Build (Recommended):**
```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first (better caching)
COPY package*.json ./
RUN npm ci --only=production

# Copy source and build
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-alpine AS production

# Security: Run as non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

WORKDIR /app

# Copy only what's needed
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./

USER nextjs

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "dist/main.js"]
```

**Layer Optimization:**
```dockerfile
# BAD - Creates many layers, poor caching
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN rm -rf /var/lib/apt/lists/*

# GOOD - Single layer, cleanup in same layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl \
      git \
      ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean
```

### Language-Specific Dockerfiles

**Node.js:**
```dockerfile
FROM node:20-alpine

# Set production environment
ENV NODE_ENV=production

# Create non-root user
RUN addgroup -g 1001 -S app && \
    adduser -S -u 1001 -G app app

WORKDIR /app

# Install dependencies (cached if package.json unchanged)
COPY --chown=app:app package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Copy application
COPY --chown=app:app . .

USER app

EXPOSE 3000

CMD ["node", "src/index.js"]
```

**Python:**
```dockerfile
FROM python:3.12-slim

# Prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

WORKDIR /app

# Install dependencies
COPY --chown=app:app requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY --chown=app:app . .

USER app

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

**Go:**
```dockerfile
# Build stage
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Download dependencies
COPY go.mod go.sum ./
RUN go mod download

# Build binary
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /app/server ./cmd/server

# Production stage - scratch for smallest image
FROM scratch

# Import CA certificates for HTTPS
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Copy binary
COPY --from=builder /app/server /server

EXPOSE 8080

ENTRYPOINT ["/server"]
```

**PHP/Laravel:**
```dockerfile
FROM php:8.3-fpm-alpine

# Install extensions
RUN apk add --no-cache \
    libpng-dev \
    libzip-dev \
    && docker-php-ext-install \
    pdo_mysql \
    gd \
    zip \
    opcache

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

# Copy composer files first
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --no-autoloader

# Copy application
COPY . .

# Generate autoloader
RUN composer dump-autoload --optimize

# Set permissions
RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache

USER www-data

EXPOSE 9000

CMD ["php-fpm"]
```

### Docker Compose

**Development Stack:**
```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: development  # Multi-stage target
    volumes:
      - .:/app
      - node_modules:/app/node_modules
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgres://user:pass@db:5432/app
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - app-network

  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
    depends_on:
      - app
    networks:
      - app-network

volumes:
  postgres_data:
  redis_data:
  node_modules:

networks:
  app-network:
    driver: bridge
```

**Production Compose:**
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  app:
    image: ${REGISTRY}/myapp:${VERSION:-latest}
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
      rollback_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    environment:
      - NODE_ENV=production
    secrets:
      - db_password
      - api_key
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

secrets:
  db_password:
    external: true
  api_key:
    external: true
```

### Security Best Practices

**1. Non-Root User:**
```dockerfile
# Create user
RUN addgroup -g 1001 -S appgroup && \
    adduser -S -u 1001 -G appgroup appuser

# Switch to non-root
USER appuser
```

**2. Minimal Base Images:**
```dockerfile
# Size comparison (Node.js example):
# node:20        ~1GB
# node:20-slim   ~200MB
# node:20-alpine ~150MB

# Use distroless for production
FROM gcr.io/distroless/nodejs20-debian12
```

**3. Pin Versions:**
```dockerfile
# BAD - Unpredictable
FROM node:latest

# GOOD - Pinned
FROM node:20.11.0-alpine3.19
```

**4. Scan for Vulnerabilities:**
```bash
# Using Docker Scout
docker scout cves myimage:latest

# Using Trivy
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image myimage:latest

# Using Snyk
docker scan myimage:latest
```

**5. Don't Store Secrets in Images:**
```dockerfile
# BAD - Secret baked into image
ENV API_KEY=secret123

# GOOD - Use build args for non-sensitive, runtime env for secrets
ARG BUILD_VERSION
ENV APP_VERSION=${BUILD_VERSION}
# API_KEY provided at runtime via -e or secrets
```

**6. Use .dockerignore:**
```
# .dockerignore
.git
.gitignore
.env
.env.*
node_modules
npm-debug.log
Dockerfile*
docker-compose*
.dockerignore
README.md
.vscode
.idea
*.md
tests/
coverage/
.nyc_output/
```

### Health Checks

**HTTP Health Check:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
```

**TCP Health Check:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD nc -z localhost 3000 || exit 1
```

**Custom Script:**
```dockerfile
COPY healthcheck.sh /usr/local/bin/
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD /usr/local/bin/healthcheck.sh
```

### Networking

**Network Types:**
```yaml
networks:
  # Bridge (default) - Isolated network
  frontend:
    driver: bridge

  # Host - Use host networking
  hostnet:
    driver: host

  # Overlay - Multi-host (Swarm)
  backend:
    driver: overlay
    attachable: true

  # External - Pre-existing network
  existing:
    external: true
    name: my-pre-existing-network
```

**DNS Resolution:**
```yaml
services:
  app:
    # Can reach db at 'db' hostname
    depends_on:
      - db

  db:
    # Accessible as 'db' within network
    hostname: db
```

### Volume Management

**Named Volumes:**
```yaml
volumes:
  postgres_data:
    driver: local

  # NFS volume
  shared_data:
    driver: local
    driver_opts:
      type: nfs
      o: addr=nfs-server.local,rw
      device: ":/path/to/share"
```

**Bind Mounts:**
```yaml
services:
  app:
    volumes:
      # Bind mount (development)
      - ./src:/app/src:ro
      # Named volume (persistent data)
      - data:/app/data
      # tmpfs (in-memory, ephemeral)
      - type: tmpfs
        target: /app/tmp
```

### Commands Reference

```bash
# Build
docker build -t myapp:latest .
docker build -t myapp:latest --target production .
docker build --no-cache -t myapp:latest .

# Run
docker run -d --name myapp -p 3000:3000 myapp:latest
docker run -it --rm myapp:latest /bin/sh
docker run -d --env-file .env myapp:latest

# Compose
docker compose up -d
docker compose up -d --build
docker compose down -v  # Remove volumes too
docker compose logs -f app
docker compose exec app /bin/sh
docker compose ps

# Images
docker images
docker image prune -a  # Remove unused
docker tag myapp:latest registry.com/myapp:v1.0.0
docker push registry.com/myapp:v1.0.0

# Containers
docker ps -a
docker logs -f container_name
docker exec -it container_name /bin/sh
docker stats
docker inspect container_name

# Cleanup
docker system prune -a --volumes  # Remove everything unused
docker volume prune
docker network prune

# Debug
docker logs container_name --tail 100
docker exec -it container_name /bin/sh
docker inspect container_name
docker events --filter container=container_name
```

### Performance Optimization

**Build Cache:**
```dockerfile
# Order matters! Least changing first
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build
```

**BuildKit Features:**
```dockerfile
# syntax=docker/dockerfile:1

# Cache mounts (persistent cache across builds)
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Secret mounts (not stored in image)
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci
```

**Enable BuildKit:**
```bash
# Environment variable
DOCKER_BUILDKIT=1 docker build .

# Or in docker daemon config
# /etc/docker/daemon.json
{
  "features": {
    "buildkit": true
  }
}
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Build slow | Use .dockerignore, optimize layer order |
| Image too large | Multi-stage build, alpine base, remove dev deps |
| Container exits immediately | Check logs, verify CMD/ENTRYPOINT |
| Permission denied | Check USER directive, volume permissions |
| Network issues | Check network mode, expose ports correctly |
| Cannot connect to services | Use service names as hostnames in compose |

### Checklist

Before building:
- [ ] .dockerignore is comprehensive
- [ ] Using specific version tags (not `latest`)
- [ ] Multi-stage build for smaller images
- [ ] Non-root user configured
- [ ] Health check defined
- [ ] No secrets in Dockerfile
- [ ] Layers optimized for caching
- [ ] Security scan passed

## Integration

Works with:
- `/devops` - Container deployment pipelines
- `/k8s` - Kubernetes deployments
- `ci-templates` skill - CI/CD with Docker
- `/security` - Container security scanning
