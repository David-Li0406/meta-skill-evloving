---
name: jax-optimization
description: A workflow for profiling and optimizing JAX-based code performance. Use this when the goal is to improve speed or OPS (Operations Per Second), involving profiling, hypothesis formation, and benchmarking.
---

# JAX Optimization Workflow

This skill guides you through the process of profiling and optimizing JAX-based applications to ensure verifiable performance improvements without sacrificing correctness.

## When to use this skill

- Use this skill when you are tasked with improving the performance, speed, or throughput (OPS) of the codebase.
- Use this when you are investigating performance bottlenecks in JAX functions.
- Use this when working on tasks related to `profile_benchmark.py` or `test_optimize.py`.

## How to use it

Follow these six steps strictly. Do not skip establishing a baseline or profiling with data.

### 1. Establish Baseline (Do not skip)

Before changing any code, you must measure the current performance to have a valid reference.
**Constraint**: Do not edit `test_optimize.py` to make numbers look better; that is cheating!

- **Action**: Run existing benchmark.
- **Output**: OPS (Operations Per Second)

```bash
uv run python -m pytest tests/test_optimize.py --benchmark-only
```

### 2. Profile with Data (No guessing)

Do not optimize based on "static analysis" or reading code. You must "see" the bottleneck via profiling tools.

- **Action**: Use the profiling script (e.g., `scripts/profile_benchmark.py`)
- **Instrumetation**: Add profiling blocks to identify parts of the source code before profiling.

```python
@partial(jax.named_call, name="move_agent")
@jax.jit
def _move_agent(pos, current_objects, action):
    ...
```

- **Note**: `jax.jit` stops trace propagation. If you need to dive deeper, you may need to remove outer `jax.jit` blocks temporarily, but make sure you `jax.jit` the inner function you are profiling.

Example command:
```bash
uv run python scripts/profile_benchmark.py --env ForagaxDiwali-v5
```

### 3. Formulate Hypothesis & Plan

Based on the data from Step 2, clearly state what is being optimized and why. Target the most time-consuming part of the code ("the bottleneck").
Make a single optimization at a time.

- **Constraint**: When optimizing, do not change the functional correctness of the code.

### 4. Implement Optimization

Apply the targeted change to the codebase.

### 5. Verify Correctness

Speed without correctness is failure.

- **Safety**: Ensure all tests still pass to verify that functionality hasn't broken.

### 6. Verify Improvement

Prove the gain.

- **Action**: Re-run the baseline benchmark (Step 1) to confirm end-to-end speedup.
