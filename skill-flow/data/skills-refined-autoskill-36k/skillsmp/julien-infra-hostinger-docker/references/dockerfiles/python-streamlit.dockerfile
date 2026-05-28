# ==================================================
# PYTHON STREAMLIT - DOCKERFILE TEMPLATE
# ==================================================
# Multi-stage build for size reduction
# Security: non-root user
# ==================================================

# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /build

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN groupadd -r streamlit && useradd -r -g streamlit streamlit && \
    mkdir -p /app/.streamlit && \
    chown -R streamlit:streamlit /app

# Copy virtual environment from builder
COPY --from=builder --chown=streamlit:streamlit /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY --chown=streamlit:streamlit . .

# Switch to non-root user
USER streamlit

# Expose port
EXPOSE 8501

# Health check (Streamlit needs longer start period)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
