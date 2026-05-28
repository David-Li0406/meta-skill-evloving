---
name: uv-docker-integration
description: Comprehensive guidance for using uv (Python package manager) in Docker environments with best practices for multi-stage builds, caching, and optimization. Use when containerizing Python applications with uv for production deployments.
---

# uv Docker Integration Skill

## Overview
This skill provides comprehensive guidance for using uv (a Python package manager) in Docker environments. It includes best practices for multi-stage builds, caching strategies, optimization techniques, and security considerations when containerizing Python applications with uv.

## When to Use This Skill
- Containerizing Python applications with uv as the package manager
- Creating optimized Docker images with minimal size
- Implementing multi-stage builds for Python projects
- Setting up proper caching strategies for faster builds
- Following security best practices in containerized Python apps
- Using uv's pip interface within Docker containers

## Core Dockerfile Patterns

### Installing uv in Docker

#### Method 1: Copy from distroless image (Recommended)
```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
```

#### Method 2: Using the installer script
```dockerfile
FROM python:3.12-slim

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download and run the installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the PATH
ENV PATH="/root/.local/bin/:$PATH"
```

### Pinning to Specific Versions (Best Practice)
```dockerfile
# Pin to specific version
COPY --from=ghcr.io/astral-sh/uv:0.9.21 /uv /uvx /bin/

# Even better - pin to specific SHA256 hash for reproducible builds
COPY --from=ghcr.io/astral-sh/uv@sha256:2381d6aa60c326b71fd40023f921a0a3b8f91b14d5db6b90402e65a635053709 /uv /uvx /bin/
```

### Basic Project Installation Pattern
```dockerfile
# Copy the project into the image
COPY . /app

# Disable development dependencies
ENV UV_NO_DEV=1

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
RUN uv sync --locked

# Set PATH to include the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Run the application
CMD ["uv", "run", "my_app"]
```

### Multi-Stage Dockerfile with uv (Recommended Pattern)
```dockerfile
# ========================================
# Optimized Multi-Stage Dockerfile
# Python Application with uv Package Manager
# ========================================

# --- Base stage ---
FROM python:3.12-slim AS base

# Set working directory
WORKDIR /app

# Install system dependencies needed for building wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# --- Builder stage ---
FROM base AS builder

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files first for better cache usage
COPY pyproject.toml uv.lock* ./

# Create virtual environment and install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv && \
    . .venv/bin/activate && \
    uv sync --locked --no-dev

# Copy the rest of the application code
COPY src/ src/
COPY alembic/ alembic/
COPY alembic.ini ./
COPY *.md ./
COPY jwks.json ./

# --- Final stage ---
FROM python:3.12-slim AS final

# Install system dependencies needed for runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# Copy virtual environment from builder
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv

# Copy application code from builder
COPY --from=builder --chown=appuser:appuser /app/src /app/src
COPY --from=builder --chown=appuser:appuser /app/alembic /app/alembic
COPY --from=builder --chown=appuser:appuser /app/alembic.ini /app/alembic.ini
COPY --from=builder --chown=appuser:appuser /app/*.md /app/
COPY --from=builder --chown=appuser:appuser /app/jwks.json /app/jwks.json

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Expose application port
EXPOSE 8000

# Run the application
CMD ["python", "-m", "src.main:app"]
```

## Optimization Techniques

### 1. Bytecode Compilation (Production Optimization)
```dockerfile
# Enable bytecode compilation for faster startup
RUN uv sync --compile-bytecode

# Or set globally
ENV UV_COMPILE_BYTECODE=1
```

### 2. Cache Mounts for Faster Builds
```dockerfile
# Use cache mount to speed up dependency installation
ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync
```

### 3. Intermediate Layers (Improved Build Times)
Separate dependency installation from project code for better caching:

```dockerfile
# Install dependencies separately for better caching
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy project files
COPY . /app

# Install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked
```

### 4. Non-Editable Installs for Production
```dockerfile
# Use non-editable mode for final image (removes dependency on source code)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable
```

## Development Workflow

### Mounting Project for Development
```bash
# Mount project directory while excluding .venv
docker run --rm \
  --volume .:/app \
  --volume /app/.venv \
  --env UV_NO_DEV=1 \
  your-image:latest
```

### Docker Compose Watch Configuration
```yaml
services:
  app:
    build: .
    develop:
      watch:
        # Sync working directory with /app, excluding .venv
        - action: sync
          path: .
          target: /app
          ignore:
            - .venv/
        # Rebuild on changes to pyproject.toml
        - action: rebuild
          path: ./pyproject.toml
```

## Using uv's pip Interface in Docker

### Installing Packages Directly
```dockerfile
# Install to system environment (safe in containers)
RUN uv pip install --system ruff

# Or create and use a virtual environment
RUN uv venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN uv pip install ruff
```

### Installing from Requirements
```dockerfile
COPY requirements.txt .
RUN uv pip install -r requirements.txt
```

## Security Best Practices

### 1. Non-Root Users
```dockerfile
RUN useradd --create-home --shell /bin/bash appuser
USER appuser
```

### 2. Pin Image Versions
Always pin to specific uv versions or SHA256 hashes:
```dockerfile
COPY --from=ghcr.io/astral-sh/uv:0.9.21@sha256:... /uv /bin/uv
```

### 3. Verify Attestations
Use GitHub CLI to verify image provenance:
```bash
gh attestation verify --owner astral-sh oci://ghcr.io/astral-sh/uv:latest
```

## Troubleshooting Common Issues

### 1. Dependency Resolution Problems
- Ensure `uv.lock` is committed to version control
- Use `uv sync --locked` to prevent accidental upgrades
- Check that `pyproject.toml` is properly formatted

### 2. Build Cache Issues
- Use `--no-cache` flag to bypass Docker cache: `docker build --no-cache`
- Clear uv cache: `uv cache clean`
- Check cache mount permissions

### 3. Virtual Environment Issues
- Set `UV_PROJECT_ENVIRONMENT` to install to system Python environment
- Use `--no-editable` flag for production builds
- Ensure `.venv` is in `.dockerignore` to prevent conflicts

### 4. Missing Dependencies
- Use `--no-install-project` to install only dependencies
- Verify all required files are copied to the container
- Check that development dependencies are disabled in production builds

## File Recommendations

### Add to .dockerignore
```
.venv/
.env
*.pyc
__pycache__/
.git/
```

### Recommended Project Structure
```
project/
├── pyproject.toml
├── uv.lock
├── src/
│   └── my_project/
├── Dockerfile
├── docker-compose.yml
└── .dockerignore
```