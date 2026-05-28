---
name: docker-containerization
description: Use this skill for building, securing, and deploying Docker containers in development and production environments.
---

# Docker & Containerization

## Overview

This skill covers Docker containerization, multi-stage builds, Docker Compose, and best practices for building and deploying containers.

## When to Use This Skill
- Creating `Dockerfile` or `docker-compose.yml`.
- Optimizing image size and debugging container networking.
- Implementing container orchestration with Kubernetes.

## Dockerfile Best Practices

### Multi-Stage Builds
- Use multi-stage builds to keep production images small by separating build and runtime stages.
- Copy only necessary artifacts to the final image.

### Layer Optimization
- Order instructions from least to most frequently changing to leverage layer caching.
- Combine `RUN` commands to reduce layers and use `.dockerignore` to exclude unnecessary files.

### Security Best Practices
- Run containers as a non-root user.
- Use specific version tags instead of `latest`.
- Avoid storing secrets in images; use environment variables or secrets management.

### Example Dockerfile for Node.js
```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/dist ./dist
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

USER nextjs
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

## Docker Compose Patterns

### Development Environment
```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
    depends_on:
      - db
      - redis

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
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

### Production with Traefik
```yaml
version: '3.8'

services:
  app:
    image: ghcr.io/frankxai/app:latest
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app.rule=Host(`frankx.ai`)"
      - "traefik.http.routers.app.tls.certresolver=letsencrypt"

  traefik:
    image: traefik:v3.0
    command:
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.email=frank@frankx.ai"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

## Health Checks
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## Common Docker Commands
```bash
# Build image
docker build -t myapp:latest .

# Start services
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop and remove
docker-compose down
```

## Anti-Patterns
- Avoid using `:latest` tag in production.
- Do not run as root or include dev dependencies in production images.
- Ensure to use a comprehensive `.dockerignore` file.

## Useful Tools
- `lazydocker` - TUI for Docker
- `dive` - Analyze Docker image layers
- `hadolint` - Dockerfile linter