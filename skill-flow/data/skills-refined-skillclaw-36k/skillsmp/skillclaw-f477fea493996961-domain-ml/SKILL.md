---
name: domain-ml
description: Use this skill when building ML/AI applications in Rust, focusing on efficient data handling, model portability, and GPU utilization.
---

# Machine Learning Domain

> **Layer 3: Domain Constraints**

## Domain Constraints → Design Implications

| Domain Rule       | Design Constraint      | Rust Implication          |
|-------------------|------------------------|---------------------------|
| Large data        | Efficient memory       | Zero-copy, streaming      |
| GPU acceleration   | CUDA/Metal support     | candle, tch-rs           |
| Model portability  | Standard formats       | ONNX                     |
| Batch processing   | Throughput over latency | Batched inference         |
| Numerical precision | Float handling        | ndarray, careful f32/f64  |
| Reproducibility    | Deterministic         | Seeded random, versioning |

---

## Critical Constraints

### Memory Efficiency

```
RULE: Avoid copying large tensors
WHY: Memory bandwidth is a bottleneck
RUST: Use references, views, and in-place operations
```

### GPU Utilization

```
RULE: Batch operations for GPU efficiency
WHY: GPU overhead per kernel launch
RUST: Optimize batch sizes and use async data loading
```

### Model Portability

```
RULE: Use standard model formats
WHY: Train in Python, deploy in Rust
RUST: Utilize ONNX via tract or candle
```

---

## Trace Down ↓

From constraints to design (Layer 2):

```
"Need efficient data pipelines"
    ↓ m10-performance: Streaming, batching
    ↓ polars: Lazy evaluation

"Need GPU inference"
    ↓ m07-concurrency: Async data loading
    ↓ candle/tch-rs: CUDA backend

"Need model loading"
    ↓ m12-lifecycle: Lazy init, caching
    ↓ tract: ONNX runtime
```

---

## Use Case → Framework

| Use Case          | Recommended         | Why                     |
|-------------------|---------------------|-------------------------|
| Inference only    | tract (ONNX)        | Lightweight, portable    |
| Training + inference | candle, burn     | Pure Rust, GPU          |
| PyTorch models    | tch-rs              | Direct bindings         |
| Data pipelines     | polars             | Fast, lazy evaluation   |

## Key Crates

| Purpose            | Crate               |
|--------------------|---------------------|
| Tensors            | ndarray             |
| ONNX inference     | tract               |
| ML framework       | candle, burn        |
| PyTorch bindings   | tch-rs              |
| Data processing    | polars              |
| Embeddings         | fastembed           |

## Design Patterns

| Pattern            | Purpose             | Implementation          |
|--------------------|---------------------|-------------------------|
| Model loading      | Once, reuse         | `OnceLock<Model>`       |
| Batching           | Throughput          | Collect then process    |
| Streaming          | Large data          | Iterator-based          |
| GPU async          | Parallelism         | Data loading parallel to compute |