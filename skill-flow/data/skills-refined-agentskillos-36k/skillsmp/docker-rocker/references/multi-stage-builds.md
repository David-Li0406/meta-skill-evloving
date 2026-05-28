# Multi-Stage Docker Builds

Comprehensive guide to multi-stage Docker builds for Python FastAPI applications.

---

## Stage Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        BUILDER STAGE                             │
│  python:3.12-slim + UV + dependencies + compile                  │
│  Size: ~400MB (discarded after build)                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        RUNTIME STAGE                             │
│  python:3.12-slim + .venv (copied) + app code                    │
│  Size: ~150MB (production image)                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        TESTING STAGE                             │
│  Extends builder + dev dependencies + pytest                     │
│  Size: ~450MB (CI/CD only)                                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Stage 1: Builder Stage

### Purpose
- Install UV package manager
- Download and cache dependencies
- Compile Python bytecode
- Build any native extensions

### Key Configuration

```dockerfile
FROM python:3.12-slim AS builder

# Install UV from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Performance environment variables
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_NO_PROGRESS=1

WORKDIR /app

# Copy dependency files first (layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies with cache mount
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable
```

### Why These Settings?

| Setting | Purpose |
|---------|---------|
| `UV_LINK_MODE=copy` | Avoids hardlink issues between container layers |
| `UV_COMPILE_BYTECODE=1` | Pre-compiles .pyc for faster startup |
| `UV_NO_PROGRESS=1` | Cleaner build logs |
| `--mount=type=cache` | Persists UV cache across builds |
| `--locked` | Ensures exact versions from lockfile |
| `--no-dev` | Excludes development dependencies |
| `--no-editable` | Allows copying venv without source |

---

## Stage 2: Runtime Stage

### Purpose
- Minimal production image
- Only runtime artifacts
- Non-root user for security
- Health checks

### Key Configuration

```dockerfile
FROM python:3.12-slim AS runtime

# Create non-root user
RUN groupadd --gid 1000 app && \
    useradd --uid 1000 --gid app --shell /bin/bash --create-home app

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder --chown=app:app /app/.venv /app/.venv

# Copy application code
COPY --chown=app:app ./app ./app

# Set PATH to use virtual environment
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Switch to non-root user
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:80/health')"

# Expose port
EXPOSE 80

# Run FastAPI
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
```

### Runtime Environment Variables

| Variable | Value | Purpose |
|----------|-------|---------|
| `PYTHONDONTWRITEBYTECODE=1` | Skip .pyc at runtime (already compiled) |
| `PYTHONUNBUFFERED=1` | Real-time log output |
| `PATH` includes .venv/bin | Use installed packages |

---

## Stage 3: Testing Stage

### Purpose
- Run tests in CI/CD
- Include dev dependencies
- Same base as builder for consistency

### Key Configuration

```dockerfile
FROM builder AS testing

# Install dev dependencies including pytest
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Copy all source code including tests
COPY --chown=app:app . .

# Default command runs tests
CMD ["pytest", "-v", "--cov=app", "--cov-report=term-missing"]
```

### CI/CD Usage

```yaml
# GitHub Actions example
- name: Run tests
  run: |
    docker build --target testing -t app:test .
    docker run --rm app:test pytest -v
```

---

## Stage 4: Development Stage (Optional)

### Purpose
- Local development with hot-reload
- Volume mounting for live code changes
- Debug capabilities

### Key Configuration

```dockerfile
FROM python:3.12-slim AS development

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Install all dependencies including dev
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Source code mounted as volume at runtime
ENV PATH="/app/.venv/bin:$PATH"

# Development server with reload
CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose for Development

```yaml
services:
  api:
    build:
      context: .
      target: development
    volumes:
      - .:/app
      - /app/.venv  # Exclude venv from mount
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://...
```

---

## Complete Multi-Stage Dockerfile

```dockerfile
# ============================================
# STAGE 1: Builder
# ============================================
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable

# ============================================
# STAGE 2: Runtime (Production)
# ============================================
FROM python:3.12-slim AS runtime

RUN groupadd --gid 1000 app && \
    useradd --uid 1000 --gid app --shell /bin/bash --create-home app

WORKDIR /app

COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --chown=app:app ./app ./app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER app

EXPOSE 80

CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]

# ============================================
# STAGE 3: Testing (CI/CD)
# ============================================
FROM builder AS testing

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

COPY . .

CMD ["pytest", "-v"]
```

---

## Build Commands

```bash
# Production image
docker build --target runtime -t myapp:prod .

# Testing image
docker build --target testing -t myapp:test .

# Development image
docker build --target development -t myapp:dev .

# Build with build args
docker build --target runtime \
    --build-arg PYTHON_VERSION=3.12 \
    -t myapp:prod .
```

---

## Layer Caching Best Practices

### Order of Operations (Most Stable → Most Volatile)

1. Base image selection
2. System package installation
3. UV/package manager installation
4. Dependency file copy (pyproject.toml, uv.lock)
5. Dependency installation
6. Application code copy
7. Configuration

### Cache Invalidation

```dockerfile
# BAD: Any file change invalidates cache
COPY . .
RUN uv sync

# GOOD: Only dependency changes invalidate sync
COPY pyproject.toml uv.lock ./
RUN uv sync
COPY ./app ./app
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Cache not working | Verify layer order, use `--mount=type=cache` |
| Large image size | Check you're copying from builder, not including source |
| Module not found | Verify PATH includes .venv/bin |
| Permission denied | Use `--chown` on COPY, run as non-root |
| Slow builds | Add cache mounts, order layers by volatility |
