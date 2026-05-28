# Docker Optimization Strategies

Strategies to minimize image size, reduce build time, and maximize performance.

---

## Image Size Optimization

### Base Image Selection

| Image | Size | Use Case |
|-------|------|----------|
| `python:3.12` | ~1GB | Never use in production |
| `python:3.12-slim` | ~150MB | Recommended for most cases |
| `python:3.12-alpine` | ~50MB | Smaller but compatibility issues |

**Recommendation**: Use `python:3.12-slim` for balance of size and compatibility.

### Size Reduction Techniques

```dockerfile
# 1. Multi-stage builds (50-70% reduction)
FROM python:3.12-slim AS builder
# ... build steps
FROM python:3.12-slim AS runtime
COPY --from=builder /app/.venv /app/.venv

# 2. Exclude dev dependencies
RUN uv sync --locked --no-dev

# 3. Clean package manager cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Use .dockerignore
# See assets/templates/.dockerignore
```

### Measuring Image Size

```bash
# Check image size
docker images myapp:latest

# Analyze layers
docker history myapp:latest

# Detailed analysis with dive
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive myapp:latest
```

---

## Build Time Optimization

### UV Cache Mounts

```dockerfile
# Cache UV downloads across builds (50-70% faster)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev
```

### BuildKit Features

```bash
# Enable BuildKit (faster, parallel builds)
export DOCKER_BUILDKIT=1

# Or in docker-compose
# compose.yml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    x-bake:
      cache-from:
        - type=local,src=/tmp/.buildx-cache
      cache-to:
        - type=local,dest=/tmp/.buildx-cache
```

### Layer Order Optimization

```dockerfile
# CORRECT ORDER (fastest rebuilds)

# 1. Rarely changes
FROM python:3.12-slim AS builder

# 2. Rarely changes
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 3. Rarely changes
ENV UV_LINK_MODE=copy

# 4. Occasionally changes
COPY pyproject.toml uv.lock ./

# 5. Occasionally changes
RUN uv sync --locked --no-dev

# 6. Frequently changes (last!)
COPY ./app ./app
```

### Parallel Stage Builds

```bash
# Build multiple targets in parallel
docker buildx bake --file docker-bake.hcl

# docker-bake.hcl
group "default" {
  targets = ["runtime", "testing"]
}

target "runtime" {
  dockerfile = "Dockerfile"
  target = "runtime"
  tags = ["myapp:prod"]
}

target "testing" {
  dockerfile = "Dockerfile"
  target = "testing"
  tags = ["myapp:test"]
}
```

---

## Runtime Performance

### Bytecode Compilation

```dockerfile
# Compile at build time (faster startup)
ENV UV_COMPILE_BYTECODE=1

# Or manually
RUN python -m compileall -q /app
```

### Worker Configuration

```dockerfile
# Single worker (container orchestration handles scaling)
CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# Multiple workers (standalone deployment)
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]

# Auto-detect workers based on CPU
CMD ["gunicorn", "-w", "$(nproc)", "-k", "uvicorn.workers.UvicornWorker", "app.main:app"]
```

### Memory Optimization

```dockerfile
# Limit Python memory
ENV PYTHONMALLOC=malloc
ENV MALLOC_TRIM_THRESHOLD_=100000

# In docker-compose or runtime
deploy:
  resources:
    limits:
      memory: 512M
    reservations:
      memory: 256M
```

---

## UV-Specific Optimizations

### Environment Variables

```dockerfile
ENV UV_LINK_MODE=copy \           # Avoid hardlink issues
    UV_COMPILE_BYTECODE=1 \       # Pre-compile for speed
    UV_NO_PROGRESS=1 \            # Clean logs
    UV_FROZEN=1 \                 # Fail if lockfile outdated
    UV_NO_CACHE=0                 # Enable caching
```

### Lockfile Validation

```dockerfile
# Fail build if lockfile is outdated
RUN uv sync --locked --no-dev

# Or strict mode
RUN uv sync --frozen --no-dev
```

### Non-Editable Install

```dockerfile
# Allows copying venv without source code
RUN uv sync --locked --no-dev --no-editable

# In runtime stage, only copy venv (not source)
COPY --from=builder /app/.venv /app/.venv
```

---

## .dockerignore Best Practices

```dockerignore
# Version control
.git
.gitignore

# Python artifacts
__pycache__
*.py[cod]
*$py.class
*.so
.Python
*.egg-info
.eggs

# Virtual environments
.venv
venv
ENV

# IDE
.idea
.vscode
*.swp
*.swo

# Testing
.pytest_cache
.coverage
htmlcov
.tox

# Build artifacts
build
dist
*.egg

# Documentation
docs/_build

# Local config
.env
.env.*
*.local

# Docker
Dockerfile*
docker-compose*
.docker

# CI/CD
.github
.gitlab-ci.yml

# Misc
*.log
*.tmp
.DS_Store
Thumbs.db
```

---

## CI/CD Caching

### GitHub Actions

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    target: runtime
    push: true
    tags: myapp:latest
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

### GitLab CI

```yaml
build:
  script:
    - docker build
        --cache-from $CI_REGISTRY_IMAGE:cache
        --build-arg BUILDKIT_INLINE_CACHE=1
        -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
        .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

---

## Size Comparison Examples

| Configuration | Image Size |
|---------------|------------|
| python:3.12 + pip install | ~1.2GB |
| python:3.12-slim + pip | ~400MB |
| Multi-stage + UV + slim | ~150MB |
| Multi-stage + UV + alpine | ~80MB |

**Target**: Production images should be <200MB for fast deployments.

---

## Optimization Checklist

- [ ] Using python:3.12-slim base image
- [ ] Multi-stage build separating builder and runtime
- [ ] UV cache mounts enabled (`--mount=type=cache`)
- [ ] Bytecode compilation enabled (`UV_COMPILE_BYTECODE=1`)
- [ ] Dev dependencies excluded (`--no-dev`)
- [ ] Layer order optimized (deps before code)
- [ ] .dockerignore configured
- [ ] BuildKit enabled
- [ ] No unnecessary files in final image
- [ ] apt cache cleaned after installs
