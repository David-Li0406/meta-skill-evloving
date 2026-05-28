---
name: get-available-resources
description: Use this skill at the start of any computationally intensive scientific task to detect and report available system resources (CPU cores, GPUs, memory, disk space) and generate strategic recommendations for computational approaches.
---

# Get Available Resources

## Overview

This skill detects available computational resources and generates strategic recommendations for scientific computing tasks. It automatically identifies CPU capabilities, GPU availability (NVIDIA CUDA, AMD ROCm, Apple Silicon Metal), memory constraints, and disk space to help make informed decisions about computational approaches.

## When to Use This Skill

Use this skill proactively before any computationally intensive task:

- **Before data analysis**: Determine if datasets can be loaded into memory or require out-of-core processing.
- **Before model training**: Check if GPU acceleration is available and which backend to use.
- **Before parallel processing**: Identify the optimal number of workers for joblib, multiprocessing, or Dask.
- **Before large file operations**: Verify sufficient disk space and appropriate storage strategies.
- **At project initialization**: Understand baseline capabilities for making architectural decisions.

**Example scenarios:**
- "Help me analyze this 50GB genomics dataset" → Use this skill first to determine if Dask/Zarr are needed.
- "Train a neural network on this data" → Use this skill to detect available GPUs and backends.
- "Process 10,000 files in parallel" → Use this skill to determine the optimal worker count.
- "Run a computationally intensive simulation" → Use this skill to understand resource constraints.

## How This Skill Works

### Resource Detection

The skill runs `scripts/detect_resources.py` to automatically detect:

1. **CPU Information**
   - Physical and logical core counts
   - Processor architecture and model
   - CPU frequency information

2. **GPU Information**
   - NVIDIA GPUs: Detects via nvidia-smi, reports VRAM, driver version, compute capability.
   - AMD GPUs: Detects via rocm-smi.
   - Apple Silicon: Detects M1/M2/M3/M4 chips with Metal.
   
3. **Memory and Disk Space**
   - Reports available RAM and disk space to inform processing strategies.