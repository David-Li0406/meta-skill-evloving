---
name: devops-infrastructure
description: Use this skill when you need to implement modern DevOps practices, including containerization, orchestration, CI/CD, and infrastructure management.
---

# DevOps & Infrastructure

Comprehensive patterns for Docker, Kubernetes, CI/CD pipelines, and infrastructure-as-code.

## When to Use

- Containerizing applications with Docker
- Orchestrating containers with Kubernetes
- Setting up CI/CD pipelines (GitHub Actions, GitLab CI)
- Infrastructure as Code with Terraform
- Configuring monitoring and logging
- Managing secrets and configuration

## Docker Patterns

### Multi-Stage Build (Production)

```dockerfile
# Dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

USER nextjs

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Docker Compose (Development)

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
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
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app

volumes:
  postgres_data:
  redis_data:
```

### Docker Best Practices

```dockerfile
# Use specific versions, not :latest
FROM node:20.11.0-alpine3.19

# Minimize layers by combining RUN commands
RUN apk add --no-cache \
    git \
    curl \
    && rm -rf /var/cache/apk/*

# Use .dockerignore
# .dockerignore
node_modules
.git
.env
```