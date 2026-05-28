# Multi-Stage Docker Builds for Python

## Stage Architecture

Python projects use 3-4 stages for optimal performance:

### Stage 1: `base` — Shared Foundation
```dockerfile
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
```
- `PYTHONDONTWRITEBYTECODE=1`: Prevents `.pyc` files (smaller image)
- `PYTHONUNBUFFERED=1`: Ensures logs appear immediately
- `python:3.12-slim`: ~150MB vs ~1GB for full image

### Stage 2: `builder` — Dependencies
```dockerfile
FROM base AS builder
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install --user -r requirements.txt
```
- `--mount=type=cache`: Persists pip cache across builds
- `--mount=type=bind`: Avoids COPY layer invalidation
- `--user` install: Clean copy to production stage

### Stage 3: `dev` / `test` (Optional)
```dockerfile
FROM base AS dev
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . .
RUN pytest
```
- Targeted with `docker build --target dev`
- Never reaches production
- Runs tests, linting, type checking

### Stage 4: `production` — Minimal Runtime
```dockerfile
FROM python:3.12-slim AS production
RUN adduser --disabled-password --no-create-home appuser
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . .
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
- Fresh slim base (no build artifacts)
- Non-root user for security
- Only runtime dependencies

## Performance Techniques

| Technique | Command/Config | Benefit |
|-----------|---------------|---------|
| Cache mounts | `--mount=type=cache,target=/root/.cache/pip` | Reuses downloaded packages |
| Bind mounts | `--mount=type=bind,source=requirements.txt,target=requirements.txt` | No COPY layer for requirements |
| Layer ordering | Install deps BEFORE copying source | Code changes don't reinstall deps |
| Slim base | `python:3.12-slim` | ~150MB vs ~1GB |
| BuildKit | `DOCKER_BUILDKIT=1` | Parallel stages, skips unused |
| .dockerignore | Exclude `.git`, `__pycache__`, `.venv`, `node_modules` | Smaller build context |
| Version pinning | `FROM python:3.12.4-slim@sha256:...` | Reproducible builds |

## Build Commands

```bash
# Production (default, skips dev/test)
docker build -t username/app:v1.0 .

# Development (stops at dev stage)
docker build --target dev -t app:dev .

# Force fresh build
docker build --pull --no-cache -t username/app:v1.0 .

# Multi-platform
docker buildx build --platform linux/amd64,linux/arm64 -t username/app:v1.0 --push .
```

## Anti-Patterns to Avoid

| Anti-Pattern | Correct Approach |
|--------------|-----------------|
| `FROM python:3.12` (full image) | Use `python:3.12-slim` |
| `COPY . .` before `pip install` | Copy requirements first, install, then copy source |
| `pip install` without cache mount | Use `--mount=type=cache` |
| Running as root | `adduser` + `USER appuser` |
| No `.dockerignore` | Always exclude build artifacts |
| `apt-get install` without cleanup | Chain with `&& rm -rf /var/lib/apt/lists/*` |
| Hardcoded versions in Dockerfile | Use build args: `ARG PYTHON_VERSION=3.12` |
