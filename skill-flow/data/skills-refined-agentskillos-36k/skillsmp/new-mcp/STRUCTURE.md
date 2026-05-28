# MCP Server File Templates

## pyproject.toml

```toml
[project]
name = "{name}-mcp"
version = "0.1.0"
description = "{Name} MCP Server for Claude Assistant Platform"
requires-python = ">=3.14"
dependencies = [
    "mcp>=1.9.0",
    "fastapi>=0.115.0",
    "uvicorn>=0.34.0",
    "httpx>=0.28.0",
    "pydantic>=2.10.0",
    "pydantic-settings>=2.7.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src"]
```

## src/server.py

```python
"""
{Name} MCP Server

Provides tools for {description of what this MCP does}.
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

from src.client import {Name}Client
from src.models import {Model}Request, {Model}Response


# =============================================================================
# Configuration
# =============================================================================

{NAME}_API_KEY = os.getenv("{NAME}_API_KEY", "")
HOST = os.getenv("{NAME}_MCP_HOST", "0.0.0.0")
PORT = int(os.getenv("{NAME}_MCP_PORT", "808X"))


# =============================================================================
# FastMCP Server
# =============================================================================

mcp = FastMCP("{name}-mcp")


@mcp.tool()
async def example_tool(
    param1: str,
    param2: int = 10,
) -> dict:
    """
    Brief description of what this tool does.

    Args:
        param1: Description of this parameter.
        param2: Description with default value.

    Returns:
        Dictionary containing the result.
    """
    client = {Name}Client({NAME}_API_KEY)
    return await client.example_method(param1, param2)


# =============================================================================
# FastAPI Application
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    yield
    # Shutdown


app = FastAPI(
    title="{Name} MCP Server",
    description="MCP server for {service} integration",
    version="0.1.0",
    lifespan=lifespan,
)


# =============================================================================
# HTTP Endpoints
# =============================================================================

@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint for container orchestration."""
    return {
        "status": "healthy",
        "service": "{name}-mcp",
        "version": os.getenv("IMAGE_VERSION", "0.1.0"),
    }


class ExampleToolRequest(BaseModel):
    """Request model for example_tool HTTP endpoint."""
    param1: str
    param2: int = 10


@app.post("/tools/example_tool")
async def http_example_tool(request: ExampleToolRequest) -> dict:
    """HTTP endpoint wrapper for example_tool."""
    try:
        return await example_tool(
            param1=request.param1,
            param2=request.param2,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
```

## src/client.py

```python
"""
{Name} API Client

Wrapper for the {Service} API.
"""

import httpx
from typing import Any


class {Name}Client:
    """Client for interacting with {Service} API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.{service}.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    async def example_method(
        self,
        param1: str,
        param2: int = 10,
    ) -> dict[str, Any]:
        """
        Example API method.

        Args:
            param1: Description
            param2: Description

        Returns:
            API response as dictionary
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/endpoint",
                headers=self.headers,
                json={
                    "param1": param1,
                    "param2": param2,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()
```

## src/models.py

```python
"""
Pydantic models for {Name} MCP Server.
"""

from pydantic import BaseModel, Field


class ExampleRequest(BaseModel):
    """Request model for example endpoint."""
    param1: str = Field(..., description="Description of param1")
    param2: int = Field(default=10, ge=1, le=100, description="Description of param2")


class ExampleResponse(BaseModel):
    """Response model for example endpoint."""
    success: bool
    data: dict | None = None
    error: str | None = None
```

## Dockerfile

```dockerfile
# =============================================================================
# {Name} MCP Server - Dockerfile
# =============================================================================
# Multi-stage build for ARM64 (Orange Pi)
# =============================================================================

# Stage 1: Builder
FROM python:3.14-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen --no-dev || uv sync --no-dev

# Stage 2: Production
FROM python:3.14-slim

WORKDIR /app

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

# Install runtime dependencies (curl for health checks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy source code
COPY --chown=appuser:appuser src/ ./src/

# Set environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 808X

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:808X/health || exit 1

# Run server
CMD ["python", "-m", "src.server"]
```

## README.md

```markdown
# {Name} MCP Server

MCP server for {Service} integration in the Claude Assistant Platform.

## Features

- Tool 1: Description
- Tool 2: Description

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `{NAME}_API_KEY` | Yes | API key for {Service} |
| `{NAME}_MCP_HOST` | No | Server bind address (default: 0.0.0.0) |
| `{NAME}_MCP_PORT` | No | Server port (default: 808X) |

## Local Development

```bash
cd MCPS/{name}
uv sync
uv run python -m src.server
```

## Health Check

```bash
curl http://localhost:808X/health
```

## Available Tools

### example_tool

Description of what this tool does.

**Parameters:**
- `param1` (string, required): Description
- `param2` (integer, optional): Description (default: 10)

**Returns:** Description of return value
```
