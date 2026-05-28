# Dockerfile Reference

Complete guide to Dockerfile instructions for Python developers.

---

## Dockerfile Basics

A Dockerfile is a text file with instructions to build an image.

```dockerfile
# This is a comment
INSTRUCTION arguments
```

**Rules**:
- Instructions are UPPERCASE (convention)
- Each instruction creates a layer
- Order matters for caching
- Comments start with `#`

---

## Essential Instructions

### FROM - Base Image

```dockerfile
# Start from an official image
FROM python:3.12-slim

# Can use specific version
FROM python:3.12.1-slim

# Can use digest for exact reproducibility
FROM python:3.12-slim@sha256:abc123...
```

**Available Python Images**:

| Tag | Size | Use Case |
|-----|------|----------|
| `python:3.12` | ~1GB | Development (has build tools) |
| `python:3.12-slim` | ~150MB | Production (recommended) |
| `python:3.12-alpine` | ~50MB | Minimal (may have compatibility issues) |

**Recommendation**: Use `python:3.12-slim` for most cases.

---

### WORKDIR - Set Directory

```dockerfile
# Set working directory
WORKDIR /app

# All subsequent commands run from /app
# Creates directory if it doesn't exist
```

**Python analogy**: Like `os.chdir('/app')` + `os.makedirs('/app')`

---

### COPY - Copy Files

```dockerfile
# Copy single file
COPY requirements.txt .

# Copy directory
COPY ./app ./app

# Copy with different name
COPY local_file.txt /app/renamed.txt

# Copy multiple files
COPY file1.txt file2.txt ./

# Copy with ownership (for non-root user)
COPY --chown=app:app . .
```

**Best Practice**: Copy files that change LESS often first.

```dockerfile
# GOOD: Dependencies change less than code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# BAD: Any code change invalidates pip install cache
COPY . .
RUN pip install -r requirements.txt
```

---

### RUN - Execute Commands

```dockerfile
# Run shell command
RUN pip install -r requirements.txt

# Run multiple commands (one layer)
RUN apt-get update && \
    apt-get install -y gcc && \
    rm -rf /var/lib/apt/lists/*

# Run with different shell
RUN ["/bin/bash", "-c", "echo hello"]
```

**Important**: Each RUN creates a new layer. Combine related commands.

```dockerfile
# BAD: 3 layers
RUN apt-get update
RUN apt-get install -y gcc
RUN rm -rf /var/lib/apt/lists/*

# GOOD: 1 layer (smaller image)
RUN apt-get update && \
    apt-get install -y gcc && \
    rm -rf /var/lib/apt/lists/*
```

---

### ENV - Environment Variables

```dockerfile
# Set single variable
ENV PYTHONUNBUFFERED=1

# Set multiple variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1
```

**Common Python Environment Variables**:

| Variable | Value | Purpose |
|----------|-------|---------|
| `PYTHONUNBUFFERED` | `1` | Real-time log output |
| `PYTHONDONTWRITEBYTECODE` | `1` | No .pyc files |
| `PIP_NO_CACHE_DIR` | `1` | Smaller image |
| `PIP_DISABLE_PIP_VERSION_CHECK` | `1` | Faster pip |

---

### EXPOSE - Document Port

```dockerfile
# Document that app uses port 8000
EXPOSE 8000

# Multiple ports
EXPOSE 8000 443
```

**Note**: EXPOSE doesn't actually publish the port! It's documentation.
You still need `-p 8000:8000` when running.

---

### CMD - Default Command

```dockerfile
# Exec form (RECOMMENDED)
CMD ["python", "main.py"]
CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# Shell form (avoid - breaks signal handling)
CMD python main.py
```

**Why Exec Form?**
- Proper signal handling (graceful shutdown)
- No shell wrapping
- More predictable

**CMD vs RUN**:

| Instruction | When | Example |
|-------------|------|---------|
| `RUN` | During BUILD | Install packages |
| `CMD` | During RUN | Start application |

---

### ENTRYPOINT - Fixed Command

```dockerfile
# Container always runs Python
ENTRYPOINT ["python"]

# CMD provides default arguments
CMD ["app.py"]

# docker run myimage → python app.py
# docker run myimage test.py → python test.py
```

**ENTRYPOINT vs CMD**:

| | ENTRYPOINT | CMD |
|---|------------|-----|
| Purpose | Fixed executable | Default arguments |
| Override | `--entrypoint` | Just add arguments |
| Common use | Wrapper scripts | Application command |

---

### ARG - Build-time Variables

```dockerfile
# Define build argument
ARG PYTHON_VERSION=3.12

# Use it
FROM python:${PYTHON_VERSION}-slim

# Build with different version
# docker build --build-arg PYTHON_VERSION=3.11 .
```

**ARG vs ENV**:

| | ARG | ENV |
|---|-----|-----|
| Available | During build only | Build and runtime |
| Override | `--build-arg` | `-e` or `--env` |
| Use case | Version selection | App configuration |

---

### USER - Run as Non-Root

```dockerfile
# Create user
RUN useradd --create-home app

# Switch to user
USER app

# All subsequent commands run as 'app'
```

**Security Best Practice**: Always run as non-root in production.

---

### HEALTHCHECK - Container Health

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Or with Python
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
```

**Options**:

| Option | Default | Purpose |
|--------|---------|---------|
| `--interval` | 30s | Time between checks |
| `--timeout` | 30s | Max time for check |
| `--retries` | 3 | Failures before unhealthy |
| `--start-period` | 0s | Grace period at start |

---

## Complete Examples

### Simple Python Script

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

### FastAPI Application

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY ./app ./app

# Environment
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Run FastAPI
CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
```

### Production FastAPI (Multi-stage)

```dockerfile
# Stage 1: Builder
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable

# Stage 2: Runtime
FROM python:3.12-slim AS runtime

RUN useradd --create-home app

WORKDIR /app

COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --chown=app:app ./app ./app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

USER app

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:80/health')"

EXPOSE 80

CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
```

---

## .dockerignore

Create `.dockerignore` to exclude files from build context:

```dockerignore
# Version control
.git
.gitignore

# Python
__pycache__
*.py[cod]
.venv
venv

# IDE
.idea
.vscode

# Testing
.pytest_cache
.coverage
htmlcov

# Build
dist
build
*.egg-info

# Docker
Dockerfile*
docker-compose*

# Environment
.env
.env.*
```

**Why?**
- Faster builds (less data to send)
- Smaller images (no unnecessary files)
- Security (no secrets copied accidentally)

---

## Common Patterns

### Install System Dependencies

```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*
```

### Cache pip Downloads

```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

### Copy Only What's Needed

```dockerfile
# Instead of COPY . .
COPY pyproject.toml .
COPY app/ app/
```

### Set Proper Permissions

```dockerfile
RUN useradd --create-home app
COPY --chown=app:app . .
USER app
```
