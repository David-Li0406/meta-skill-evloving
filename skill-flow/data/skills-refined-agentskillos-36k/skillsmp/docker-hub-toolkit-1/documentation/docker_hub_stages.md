# Multi-Stage Docker Build Stages for Python

A well-optimized Python Dockerfile typically uses **3-4 stages** to maximize performance and minimize image size.

---

## Stage 1: `base` — Shared Foundation

```dockerfile
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
```

- Sets environment variables to prevent `.pyc` files and ensure unbuffered output
- Uses `python:3.12-slim` (not full image) to reduce size
- Shared by all subsequent stages

---

## Stage 2: `builder` / `dependencies` — Install Dependencies

```dockerfile
FROM base AS builder
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install --user -r requirements.txt
```

- Installs all Python dependencies with **cache mounts** (`--mount=type=cache`) for faster rebuilds
- Uses **bind mounts** for `requirements.txt` to avoid COPY layer invalidation
- Installs to `--user` or a virtual env so dependencies can be copied cleanly

---

## Stage 3: `test` / `dev` (Optional) — Development/Testing

```dockerfile
FROM base AS dev
COPY --from=builder /root/.local /root/.local
COPY . .
RUN pytest
```

- Copies dependencies from builder stage
- Runs tests, linting, or other dev-only tools
- **Never reaches production** — targeted with `--target dev`

---

## Stage 4: `production` / `final` — Minimal Runtime

```dockerfile
FROM python:3.12-slim AS production
RUN adduser --disabled-password appuser
COPY --from=builder /root/.local /root/.local
COPY . .
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- Fresh slim base (no build tools)
- Copies **only** runtime dependencies from builder
- Runs as non-root user for security
- Minimal attack surface

---

## Key Performance & Speed Optimizations

| Technique | Benefit |
|-----------|---------|
| **`--mount=type=cache`** | Caches pip downloads across builds |
| **`--mount=type=bind`** | Avoids unnecessary COPY layers |
| **Separate dependency install** | Layer caching — code changes don't reinstall deps |
| **Slim/Alpine base images** | Final image under 100MB vs 1GB+ for full Python |
| **Multi-stage COPY --from** | Only runtime artifacts reach production |
| **`.dockerignore`** | Excludes `.git`, `__pycache__`, `.venv` from build context |
| **BuildKit** | Parallel stage processing, skips unused stages |
| **Pin versions** | Reproducible builds with digest pinning |

---

## Build Commands

```bash
# Production build (skips dev/test stages automatically)
docker build -t myapp:prod .

# Development build (stops at dev stage)
docker build --target dev -t myapp:dev .

# Force fresh build
docker build --pull --no-cache -t myapp:prod .
```

---

## Core Principle

**Separate what you need to BUILD the app from what you need to RUN it.** Build tools, compilers, test frameworks, and dev dependencies never reach the final production image.

---

## Sources

- [Docker Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Docker Python Containerization Guide](https://docs.docker.com/guides/python/containerize/)
- [Docker Build Cache](https://docs.docker.com/build/cache/)
- [Dockerfile Best Practices](https://docs.docker.com/build/building/best-practices/)
