---
title: Reset GPU State Between Inference Phases
impact: MEDIUM
impactDescription: Prevents memory pressure and OOM on 16GB systems
tags: gpu, memory, metal, mps, macos, ffi
---

## Reset GPU State Between Inference Phases

**Impact: MEDIUM** — Prevents memory accumulation and OOM on constrained systems.

> **Platform Note:** This rule documents **Apple Metal/MPS memory management** (macOS only). The `mps.reset()` shown is a conceptual API - actual implementation requires FFI calls to Metal APIs. For native Mojo GPU programming (NVIDIA/AMD), use `DeviceContext` memory management. The principle of clearing caches between inference phases applies universally.

GPU caches (weight buffers, compiled graphs) accumulate during inference. Reset state between independent phases to free memory.

**Incorrect (no reset between phases):**

```mojo
fn inference():
    text_encode()   # Caches text encoder weights
    # Memory still held!
    transformer()   # Adds transformer weights
    # Memory still held!
    vae_decode()    # Adds VAE weights -> OOM on 16GB!
```

**Correct (reset between phases):**

```mojo
fn inference():
    text_encode()
    mps.reset()     # Free text encoder caches
    
    transformer()
    mps.reset()     # Free transformer caches
    
    vae_decode()    # Now has memory headroom
```

**C implementation pattern:**

```c
void mps_reset(MPSContext* ctx) {
    mps_clear_weight_cache(ctx);
    mps_clear_graph_cache(ctx);
    // Device and queue preserved
}
```

**When to apply:**
- Between major model components (text encoder -> transformer -> VAE)
- When switching between models
- After completing inference before next request

**When NOT to apply:**
- Within tight loops where cache reuse is beneficial
- When weights are intentionally persistent
