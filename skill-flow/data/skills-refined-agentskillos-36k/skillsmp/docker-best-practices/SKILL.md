---
name: docker-best-practices
description: >
  Docker and container best practices. Load when writing Dockerfiles, building
  images, or containerizing applications. Triggers: Dockerfile, docker build,
  multi-stage builds, layer caching, image optimization, container security,
  or docker-compose configuration.
---

# Docker Best Practices

Production-ready Docker patterns for building efficient, secure container images.

## When This Skill MUST Be Used

**ALWAYS invoke this skill when the user's request involves ANY of these:**

- Writing or modifying Dockerfiles
- Building container images
- Optimizing image size or build time
- Container security hardening
- Multi-stage builds
- Layer caching strategies
- docker-compose configuration
- CI/CD container builds

**If you're about to write a Dockerfile, STOP and use this skill first.**

## Critical Safety Rules

**NEVER:**
- Run containers as root in production
- Store secrets in images (build args, env vars in Dockerfile)
- Use `latest` tag in production
- Copy entire directories without `.dockerignore`
- Install unnecessary packages
- Leave build tools in final image

**ALWAYS:**
- Use multi-stage builds
- Pin base image versions with digest
- Run as non-root user
- Use `.dockerignore`
- Scan images for vulnerabilities
- Use minimal base images (distroless, alpine)

## Quick Reference

| Task | Command |
|------|---------|
| Build image | `docker build -t app:v1 .` |
| Build with no cache | `docker build --no-cache -t app:v1 .` |
| List images | `docker images` |
| Image history | `docker history app:v1` |
| Scan for vulnerabilities | `docker scout cves app:v1` |
| Inspect image | `docker inspect app:v1` |
| Remove dangling images | `docker image prune` |

---

# Multi-Stage Builds

## Why Multi-Stage?

- Smaller final image (no build tools)
- Faster deployments
- Reduced attack surface
- Separate build and runtime concerns

## Go Application

```dockerfile
# Stage 1: Build
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Cache dependencies
COPY go.mod go.sum ./
RUN go mod download

# Build binary
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /app/server ./cmd/server

# Stage 2: Runtime
FROM gcr.io/distroless/static-debian12:nonroot

COPY --from=builder /app/server /server

USER nonroot:nonroot
EXPOSE 8080

ENTRYPOINT ["/server"]
```

## With Build Cache Mount (BuildKit)

```dockerfile
FROM golang:1.22-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .

# Cache Go build cache
RUN --mount=type=cache,target=/root/.cache/go-build \
    --mount=type=cache,target=/go/pkg/mod \
    CGO_ENABLED=0 go build -ldflags="-s -w" -o /app/server ./cmd/server

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=builder /app/server /server
USER nonroot:nonroot
ENTRYPOINT ["/server"]
```

---

# Layer Caching

## Order Matters

Put least-changing layers first:

```dockerfile
# 1. Base image (rarely changes)
FROM golang:1.22-alpine

# 2. System dependencies (rarely changes)
RUN apk add --no-cache git

# 3. Go dependencies (changes occasionally)
COPY go.mod go.sum ./
RUN go mod download

# 4. Source code (changes frequently)
COPY . .

# 5. Build (always runs when source changes)
RUN go build -o /app ./cmd/server
```

## Cache Invalidation

| Change | Layers Rebuilt |
|--------|----------------|
| Base image | All |
| System deps | All after |
| go.mod/go.sum | Download + build |
| Source code | Build only |

---

# Base Image Selection

## Options

| Base | Size | Use Case |
|------|------|----------|
| `scratch` | 0 MB | Static binaries only |
| `gcr.io/distroless/static` | ~2 MB | Go static binaries |
| `gcr.io/distroless/base` | ~20 MB | Need glibc |
| `alpine` | ~5 MB | Need shell, package manager |
| `debian-slim` | ~80 MB | Need full apt ecosystem |

## Recommendation by Language

| Language | Recommended Base |
|----------|------------------|
| Go (static) | `gcr.io/distroless/static-debian12:nonroot` |
| Go (CGO) | `gcr.io/distroless/base-debian12:nonroot` |
| Rust | `gcr.io/distroless/cc-debian12:nonroot` |
| Python | `python:3.12-slim` + venv |
| Node.js | `gcr.io/distroless/nodejs22-debian12` |

## Pin Versions

```dockerfile
# BAD: Unpredictable
FROM golang:latest

# GOOD: Pinned version
FROM golang:1.22-alpine

# BEST: Pinned with digest
FROM golang:1.22-alpine@sha256:abc123...
```

---

# Security Hardening

## Non-Root User

```dockerfile
# Option 1: Distroless (comes with nonroot user)
FROM gcr.io/distroless/static-debian12:nonroot
USER nonroot:nonroot

# Option 2: Alpine (create user)
FROM alpine:3.19
RUN addgroup -g 1000 app && \
    adduser -u 1000 -G app -s /bin/sh -D app
USER app:app

# Option 3: Numeric UID (most portable)
USER 65534:65534
```

## Read-Only Filesystem

```dockerfile
# In Dockerfile
USER nonroot:nonroot

# At runtime
docker run --read-only --tmpfs /tmp app:v1
```

## No Secrets in Images

```dockerfile
# BAD: Secret baked into image
ENV API_KEY=sk-secret-key
COPY .env /app/.env

# GOOD: Pass at runtime
# docker run -e API_KEY=$API_KEY app:v1

# GOOD: Use Docker secrets (Swarm/Compose)
# docker run --secret api_key app:v1
```

## Security Scanning

```bash
# Docker Scout (built-in)
docker scout cves app:v1

# Trivy
trivy image app:v1

# Grype
grype app:v1
```

---

# .dockerignore

Always create `.dockerignore`:

```gitignore
# Version control
.git
.gitignore

# IDE
.idea
.vscode
*.swp

# Build artifacts
bin/
dist/
*.exe

# Dependencies (rebuild in container)
vendor/
node_modules/

# Test and docs
*_test.go
docs/
*.md
!README.md

# Docker
Dockerfile*
docker-compose*.yml
.dockerignore

# Secrets (CRITICAL)
.env
.env.*
*.pem
*.key
credentials.json

# OS
.DS_Store
Thumbs.db
```

---

# Build Optimization

## Reduce Image Size

```dockerfile
# 1. Use minimal base
FROM gcr.io/distroless/static-debian12:nonroot

# 2. Strip debug info (Go)
RUN go build -ldflags="-s -w" -o /app ./cmd/server

# 3. Use UPX compression (optional, slower startup)
RUN upx --best /app/server

# 4. Remove unnecessary files
RUN rm -rf /var/cache/* /tmp/*
```

## Speed Up Builds

```dockerfile
# 1. Use BuildKit cache mounts
RUN --mount=type=cache,target=/root/.cache/go-build \
    go build -o /app ./cmd/server

# 2. Parallel downloads
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

# 3. Separate dependency and build steps
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build ...
```

## BuildKit Features

```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Or in daemon.json
{
  "features": {
    "buildkit": true
  }
}
```

---

# Health Checks

```dockerfile
# HTTP health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

# For distroless (no shell)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD ["/app/healthcheck"]
```

Go healthcheck binary:

```go
// cmd/healthcheck/main.go
package main

import (
    "net/http"
    "os"
)

func main() {
    resp, err := http.Get("http://localhost:8080/health")
    if err != nil || resp.StatusCode != 200 {
        os.Exit(1)
    }
}
```

---

# docker-compose

## Development Setup

```yaml
# docker-compose.yml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: builder  # Use build stage for dev
    volumes:
      - .:/app
      - go-mod-cache:/go/pkg/mod
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/app
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  go-mod-cache:
  postgres-data:
```

## Production Overrides

```yaml
# docker-compose.prod.yml
services:
  app:
    build:
      target: runtime  # Use final stage
    restart: always
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 512M
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

```bash
# Deploy with overrides
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

# CI/CD Integration

## GitHub Actions

```yaml
- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: ghcr.io/user/app:${{ github.sha }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## Tagging Strategy

```bash
# Development
app:dev
app:feature-xyz

# Staging
app:sha-abc123
app:pr-42

# Production
app:v1.2.3
app:v1.2.3-sha-abc123
```

---

# Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Large image | Build tools in final | Use multi-stage |
| Slow builds | Poor layer ordering | Put deps before source |
| Cache misses | Copying too much | Use `.dockerignore` |
| Permission denied | Running as root | Use non-root user |
| Can't exec into container | Using distroless | Use debug image variant |
| OOM during build | BuildKit cache full | `docker builder prune` |
| Vulnerabilities | Old base image | Update and scan regularly |

## Debug Distroless

```dockerfile
# Use debug variant (has shell)
FROM gcr.io/distroless/static-debian12:debug

# Then exec
docker exec -it container /busybox/sh
```

---

# Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| `FROM ubuntu:latest` | Large, unpinned | Use minimal, pin version |
| `COPY . .` first | Cache invalidation | Copy deps first |
| `RUN apt-get update && apt-get install` separate | Stale cache | Combine in one RUN |
| Multiple `RUN` for cleanup | Extra layers | Combine with `&&` |
| Build tools in final image | Large, insecure | Multi-stage |
| `USER root` | Security risk | Non-root user |
| Secrets in build args | Visible in history | Runtime env vars |

---

# Example Requests

| User Request | Action |
|--------------|--------|
| "Write a Dockerfile for Go" | Multi-stage with distroless, non-root |
| "Optimize image size" | Multi-stage, minimal base, strip binary |
| "Speed up builds" | Layer ordering, BuildKit cache mounts |
| "Secure the container" | Non-root, scan, read-only fs |
| "Set up docker-compose" | Services, healthchecks, volumes |
| "Debug distroless" | Use `:debug` variant |
| "CI/CD pipeline" | Build, scan, tag, push pattern |
