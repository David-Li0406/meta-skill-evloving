---
name: latchbio-integration
description: Use this skill when you need to build and deploy bioinformatics workflows using the Latch platform, leveraging Python decorators for serverless pipelines and integrating with Nextflow/Snakemake.
---

# LatchBio Integration

## Overview

Latch is a Python framework for building and deploying bioinformatics workflows as serverless pipelines. Built on Flyte, it allows you to create workflows with `@workflow` and `@task` decorators, manage cloud data with `LatchFile` and `LatchDir`, configure resources, and integrate with Nextflow/Snakemake pipelines.

## Core Capabilities

The Latch platform provides four main areas of functionality:

### 1. Workflow Creation and Deployment
- Define serverless workflows using Python decorators.
- Support for native Python, Nextflow, and Snakemake pipelines.
- Automatic containerization with Docker.
- Auto-generated no-code user interfaces.
- Version control and reproducibility.

### 2. Data Management
- Cloud storage abstractions (`LatchFile`, `LatchDir`).
- Structured data organization with Registry (Projects → Tables → Records).
- Type-safe data operations with links and enums.
- Automatic file transfer between local and cloud.
- Glob pattern matching for file selection.

### 3. Resource Configuration
- Pre-configured task decorators (`@small_task`, `@large_task`, `@small_gpu_task`, `@large_gpu_task`).
- Custom resource specifications (CPU, memory, GPU, storage).
- GPU support (K80, V100, A100).
- Timeout and storage configuration.
- Cost optimization strategies.

### 4. Verified Workflows
- Production-ready pre-built pipelines.
- Bulk RNA-seq, DESeq2, pathway analysis.
- AlphaFold and ColabFold for protein structure prediction.
- Single-cell tools (ArchR, scVelo, emptyDropsR).
- CRISPR analysis, phylogenetics, and more.

## Quick Start

### Installation and Setup

```bash
# Install Latch SDK
python3 -m uv pip install latch

# Login to Latch
latch login

# Initialize a new workflow
latch init my-workflow

# Register workflow to platform
latch register my-workflow
```

**Prerequisites:**
- Docker installed and running.
- Latch account credentials.
- Python 3.8+.

### Basic Workflow Example

```python
from latch import workflow, small_task
from latch.types import LatchFile

@small_task
def process_file(input_file: LatchFile) -> LatchFile:
    """Process a single file"""
    # Processing logic
    return output_file

@workflow
def my_workflow(input_file: LatchFile) -> LatchFile:
    """
    My bioinformatics workflow

    Args:
        input_file: Input data file
    """
    return process_file(input_file)
```