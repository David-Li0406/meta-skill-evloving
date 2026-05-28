---
name: modal
description: Use this skill when you need to run Python code in the cloud with serverless containers, GPUs, and autoscaling for tasks like deploying ML models, running batch jobs, or serving APIs.
---

# Modal

## Overview

Modal is a serverless platform for running Python code in the cloud with minimal configuration. Execute functions on powerful GPUs, scale automatically to thousands of containers, and pay only for compute used. Modal is particularly suited for AI/ML workloads, high-performance batch processing, scheduled jobs, GPU inference, and serverless APIs. Sign up for free at [modal.com](https://modal.com) and receive $30/month in credits.

## When to Use This Skill

Use Modal for:
- Deploying and serving ML models (LLMs, image generation, embedding models)
- Running GPU-accelerated computation (training, inference, rendering)
- Batch processing large datasets in parallel
- Scheduling compute-intensive jobs (daily data processing, model training)
- Building serverless APIs that need automatic scaling
- Scientific computing requiring distributed compute or specialized hardware

## Authentication and Setup

Modal requires authentication via API token.

### Initial Setup

```bash
# Install Modal
uv uv pip install modal

# Authenticate (opens browser for login)
modal token new
```

This creates a token stored in `~/.modal.toml`. The token authenticates all Modal operations.

### Verify Setup

```python
import modal

app = modal.App("test-app")

@app.function()
def hello():
    print("Modal is working!")
```

Run with: `modal run script.py`

## Core Capabilities

Modal provides serverless Python execution through Functions that run in containers. Define compute requirements, dependencies, and scaling behavior declaratively.

### 1. Define Container Images

Specify dependencies and environment for functions using Modal Images.

```python
import modal

# Basic image with Python packages
image = (
    modal.Image.debian_slim(python_version="3.12")
    .uv_pip_install("torch", "transformers", "numpy")
)

app = modal.App("ml-app", image=image)
```

**Common patterns:**
- Install Python packages: `.uv_pip_install("pandas", "scikit-learn")`
- Install system packages: `.apt_install("ffmpeg", "git")`
- Use existing Docker images: `modal.Image.from_registry("nvidia/cuda:12.1.0-base")`
- Add local code: `.add_local_python_source("my_module")`