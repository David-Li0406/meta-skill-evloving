---
name: modaljob
description: Submit Python functions to Modal with job tracking using the ModalJob decorator. Use when user wants to run GPU workloads, training jobs, or long-running tasks on Modal.
---

# ModalJob - Modal Job Submission with Tracking

A single-file decorator for submitting Python functions to [Modal](https://modal.com) with job tracking, artifact storage, and cross-session persistence.

## When to Use

Use ModalJob when:
- Running GPU workloads (training, inference, batch processing)
- Submitting long-running jobs that may outlive the current session
- Need to track job status and download artifacts later

## Quick Start

Copy `modaljob.py` into the project (see [reference](references/modaljob.py)), then:

```python
from modaljob import ModalJob, JobHandle
import modal

@ModalJob(
    image=modal.Image.debian_slim().pip_install("torch"),
    gpu="A10G",
    secrets=["wandb"],
)
def train(config):
    # Write artifacts to /outputs
    with open("/outputs/metrics.json", "w") as f:
        json.dump({"loss": 0.5}, f)
    return {"done": True}

# Submit job
handle = train.submit(config={"lr": 1e-4})
print(f"Job ID: {handle.job_id}")  # Save this to resume later
```

## Resume Jobs Across Sessions

```python
from modaljob import JobHandle

handle = JobHandle.from_id("a1b2c3d4")
print(handle.status())  # "running" | "completed" | "failed"
result = handle.result(timeout=3600)
handle.download("./outputs/")
```

## API Reference

### `@ModalJob` Decorator

```python
@ModalJob(
    image=modal.Image,      # Modal image with dependencies
    gpu="A10G",             # GPU type: "T4", "A10G", "A100-40GB", etc.
    secrets=["wandb"],      # Modal secret names
    timeout=3600,           # Max runtime in seconds
    cpu=None,               # CPU cores (optional)
    memory=None,            # Memory in MB (optional)
)
```

### `JobHandle` Methods

| Method | Description |
|--------|-------------|
| `JobHandle.from_id(job_id)` | Reconstruct handle from saved job ID |
| `handle.status()` | Poll status: "pending", "running", "completed", "failed" |
| `handle.result(timeout=None)` | Block until complete, return result |
| `handle.download(local_path)` | Download `/outputs/` artifacts |

### Utility Functions

```python
from modaljob import list_jobs

# List recent jobs
jobs = list_jobs(limit=50)
for job in jobs:
    print(f"{job.job_id}: {job.status}")
```

## Artifact Storage

Functions write to `/outputs/` which is backed by a Modal Volume:

```python
@ModalJob(...)
def my_job():
    # These files persist and can be downloaded later
    with open("/outputs/model.pt", "wb") as f:
        torch.save(model.state_dict(), f)
    with open("/outputs/metrics.json", "w") as f:
        json.dump(metrics, f)
```

## Requirements

- Python 3.12+
- `modal` package installed
- Modal account with CLI configured (`modal setup`)

## Common Patterns

### Training with WandB

```python
@ModalJob(
    image=modal.Image.debian_slim().pip_install("torch", "wandb"),
    gpu="A10G",
    secrets=["wandb"],
)
def train(config):
    import wandb
    wandb.init(project="my-project", config=config)
    # ... training code ...
    wandb.finish()
```

### Batch Inference

```python
@ModalJob(
    image=modal.Image.debian_slim().pip_install("transformers", "torch"),
    gpu="A10G",
)
def batch_inference(inputs):
    from transformers import pipeline
    pipe = pipeline("text-generation", model="meta-llama/Llama-2-7b")
    results = [pipe(x) for x in inputs]
    with open("/outputs/results.json", "w") as f:
        json.dump(results, f)
    return results
```
