# FastAPI Dockerfile for fly.io

FROM python:3.12-slim AS base

# Prevents Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
FROM base AS builder

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Production runner
FROM base AS runner

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1001 fastapi && \
    chown -R fastapi:fastapi /app

# Copy virtual environment from builder
COPY --from=builder --chown=fastapi:fastapi /opt/venv /opt/venv

# Copy application code
COPY --chown=fastapi:fastapi . .

# Set PATH to use virtual environment
ENV PATH="/opt/venv/bin:$PATH"

USER fastapi

EXPOSE 8080

ENV PORT=8080

# Run with uvicorn
# Adjust the command based on your app structure:
# - main:app if your file is main.py with app = FastAPI()
# - app.main:app if your file is app/main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

# For production with multiple workers, use:
# CMD ["gunicorn", "main:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]
