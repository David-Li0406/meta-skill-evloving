---
name: docker
description: Create Dockerfiles, Docker Compose files, optimize containers, and troubleshoot Docker issues. Use for containerization and Docker operations.
allowed-tools: Read, Write, Bash
---

# Docker Skill

Comprehensive Docker assistance.

## 1. Dockerfile Creation

**Basic Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
```

**Multi-stage Build:**
```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

## 2. Docker Compose

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://db:5432/myapp
    depends_on:
      - db
    volumes:
      - ./app:/app
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

## 3. Optimization

**Reduce Image Size:**
```dockerfile
# Use slim/alpine images
FROM python:3.11-alpine

# Multi-stage builds
FROM node:18 AS builder
# ... build steps ...
FROM node:18-alpine
COPY --from=builder /app/dist ./dist

# Minimize layers
RUN apt-get update && \
    apt-get install -y package1 package2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Use .dockerignore
# Create .dockerignore file:
node_modules
.git
*.md
.env
```

## 4. Common Commands

```bash
# Build image
docker build -t myapp:latest .

# Run container
docker run -d -p 8000:8000 --name myapp myapp:latest

# View logs
docker logs -f myapp

# Execute command
docker exec -it myapp bash

# Stop/remove
docker stop myapp
docker rm myapp

# Clean up
docker system prune -a
docker volume prune
```

## 5. Docker Compose Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild
docker-compose up -d --build

# Scale services
docker-compose up -d --scale app=3
```

## When to Use This Skill

Use `/docker` for creating Dockerfiles, Docker Compose configurations, and container optimization.
