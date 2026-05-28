---
name: wafer-guide
description: GPU kernel development with the Wafer CLI. Use when working on CUDA/HIP kernels, profiling GPU code, or optimizing kernel performance.
---

# Wafer CLI

GPU development primitives for optimizing CUDA and HIP kernels.

## Installation

Before using Wafer CLI commands, install the tool:

```bash
# Install wafer-cli using uv (recommended)
uv tool install wafer-cli

# Authenticate (one-time setup)
wafer login

```

## When to Use This Skill

Activate this skill when:
- Writing or optimizing CUDA/HIP kernels
- Profiling GPU code with NCU, NSYS, or ROCprof
- Evaluating kernel correctness and performance
- Looking up GPU programming documentation (CUDA, CUTLASS, HIP)

## Core Workflows

### 1. Documentation Lookup

Query indexed GPU documentation:

```bash
# Download corpus (one-time)
wafer corpus download cuda
wafer corpus download cutlass
wafer corpus download hip

# Query documentation
wafer wevin -t ask-docs --corpus cuda "What is warp divergence?"
wafer wevin -t ask-docs --corpus cutlass "What is a TiledMma?"
```

### 2. Trace Analysis

Analyze NCU, NSYS, or PyTorch profiler traces:

```bash
# AI-assisted analysis
wafer wevin -t trace-analyze --args trace=./profile.ncu-rep "Why is this kernel slow?"

# Direct trace queries (PyTorch/Perfetto JSON)
wafer nvidia perfetto query trace.json \
  "SELECT name, dur/1e6 as ms FROM slice WHERE cat='kernel' ORDER BY dur DESC LIMIT 10"

# NCU/NSYS analysis
wafer nvidia ncu analyze profile.ncu-rep
wafer nvidia nsys analyze profile.nsys-rep
```

### 3. Kernel Evaluation

Test correctness and measure speedup against a reference:

```bash
# Generate template files
wafer evaluate make-template ./my-kernel
# Creates: kernel.py, reference.py, test_cases.json

# Run evaluation on a configured target
wafer evaluate \
  --impl ./my-kernel/kernel.py \
  --reference ./my-kernel/reference.py \
  --test-cases ./my-kernel/test_cases.json \
  --target <target-name>

# With profiling
wafer evaluate ... --profile
```

### 4. AI-Assisted Optimization

Iteratively optimize a kernel with evaluation feedback:

```bash
wafer wevin -t optimize-kernel \
  --args kernel=./my_kernel.cu \
  --args target=H100 \
  "Optimize this GEMM for memory bandwidth"
```

### 5. Remote Execution

Run on cloud GPU workspaces:

```bash
wafer workspaces list
wafer workspaces create my-workspace --gpu H100
wafer workspaces exec <id> "python train.py"
wafer workspaces ssh <id>
```

## Command Reference

| Command | Description |
|---------|-------------|
| `wafer corpus list\|download\|path` | Manage documentation corpora |
| `wafer evaluate` | Test kernel correctness/performance |
| `wafer nvidia ncu\|nsys\|perfetto` | NVIDIA profiling tools |
| `wafer amd isa\|rocprof-compute` | AMD profiling tools |
| `wafer workspaces` | Cloud GPU environments |
| `wafer wevin -t <template>` | AI-assisted workflows |
| `wafer config targets` | Configure GPU targets |

## Target Configuration

Targets define GPU access methods. Initialize with:

```bash
wafer config targets init ssh          # Your own GPU via SSH
wafer config targets init runpod       # RunPod cloud GPUs
wafer config targets init digitalocean # DigitalOcean AMD GPUs
```

Then use: `wafer evaluate --target <name> ...`
