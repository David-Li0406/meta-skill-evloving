---
id: docker-containerization
name: "Docker Containerization"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# Docker Containerization

## Overview

Docker containerization packages applications with their dependencies into standardized units for development, deployment, and scaling. Containers provide isolation, portability, and consistent environments across development, staging, and production.

## When to Use

- Deploying applications with complex dependencies
- Ensuring consistency between development and production environments
- Microservices architecture requiring isolated services
- CI/CD pipelines needing reproducible builds
- Multi-tenant applications requiring isolation

## Key Concepts

| Concept | Description |
|---------|-------------|
| Image | Read-only template with instructions for creating container |
| Container | Runnable instance of an image |
| Dockerfile | Text file with instructions to build an image |
| Layer | Each instruction in Dockerfile creates a layer |
| Registry | Storage and distribution system for images |
| Volume | Persistent data storage outside container filesystem |
| Network | Communication layer between containers |

### Image vs Container

```
Image (Blueprint)          Container (Instance)
┌─────────────────┐       ┌─────────────────┐
│ Read-only       │       │ Writable layer  │
│ Shareable       │  →    │ Isolated process│
│ Versioned       │       │ Runtime state   │
└─────────────────┘       └─────────────────┘
```

## Implementation

### Production-Ready Dockerfile (Python)

```dockerfile
# Stage 1: Build
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Production
FROM python:3.12-slim AS production

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy application code
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:application"]
```

### Production-Ready Dockerfile (Node.js)

```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Production
FROM node:20-alpine AS production

# Security: run as non-root
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001

WORKDIR /app

# Copy built assets
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder /app/package*.json ./

USER nextjs

ENV NODE_ENV=production
ENV PORT=3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

EXPOSE 3000

CMD ["node", "dist/server.js"]
```

### .dockerignore

```
# Git
.git
.gitignore

# Dependencies
node_modules
__pycache__
*.pyc
.venv
venv

# Build outputs
dist
build
*.egg-info

# IDE
.idea
.vscode
*.swp

# Testing
.coverage
htmlcov
.pytest_cache
.tox

# Environment
.env
.env.*
*.local

# Docker
Dockerfile*
docker-compose*
.docker

# Documentation
docs
*.md
!README.md

# CI/CD
.github
.gitlab-ci.yml
Jenkinsfile
```

### Container Runtime Commands

```bash
# Build image with tags
docker build -t myapp:1.0.0 -t myapp:latest .

# Build with build arguments
docker build \
    --build-arg VERSION=1.0.0 \
    --build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
    -t myapp:1.0.0 .

# Run container with resource limits
docker run -d \
    --name myapp \
    --restart unless-stopped \
    --memory 512m \
    --cpus 0.5 \
    --read-only \
    --tmpfs /tmp \
    -p 8000:8000 \
    -e DATABASE_URL=postgres://... \
    -v /data/app:/app/data:ro \
    myapp:1.0.0

# View logs
docker logs -f --tail 100 myapp

# Execute command in running container
docker exec -it myapp /bin/sh

# Inspect container
docker inspect myapp

# Resource usage
docker stats myapp
```

### Security Scanning

```bash
# Scan image for vulnerabilities with Trivy
docker run --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    aquasec/trivy:latest image myapp:1.0.0

# Scan with severity filter
docker run --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    aquasec/trivy:latest image \
    --severity HIGH,CRITICAL \
    --exit-code 1 \
    myapp:1.0.0
```

## Best Practices

1. **Use multi-stage builds** - Reduce final image size by separating build and runtime stages
2. **Run as non-root user** - Create dedicated user with minimal permissions
3. **Pin base image versions** - Use specific tags (python:3.12.1-slim) not just (python:latest)
4. **Minimize layers** - Combine RUN commands with && to reduce layer count
5. **Order instructions by change frequency** - Put rarely changing instructions first for better caching
6. **Use .dockerignore** - Exclude unnecessary files from build context
7. **Add health checks** - Enable orchestrators to monitor container health
8. **Set resource limits** - Prevent containers from consuming excessive resources
9. **Scan for vulnerabilities** - Integrate security scanning in CI/CD pipeline
10. **Use read-only filesystem** - Mount root filesystem as read-only when possible

## Common Pitfalls

1. **Running as root** - Containers run as root by default, creating security risks. Always create and use non-root users.

2. **Using :latest tag** - Leads to unpredictable deployments. Always use specific version tags.

3. **Storing secrets in images** - Secrets in Dockerfile or environment variables are visible. Use secrets management (Docker secrets, Vault).

4. **Large image sizes** - Including build tools in production image. Use multi-stage builds to keep images small.

5. **Ignoring layer caching** - Copying all files before installing dependencies invalidates cache. Copy dependency files first.

6. **No health checks** - Orchestrators cannot detect unhealthy containers. Always include HEALTHCHECK instruction.

## References

- [Docker Documentation](https://docs.docker.com/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Security](https://docs.docker.com/engine/security/)
- [Trivy Security Scanner](https://aquasecurity.github.io/trivy/)
