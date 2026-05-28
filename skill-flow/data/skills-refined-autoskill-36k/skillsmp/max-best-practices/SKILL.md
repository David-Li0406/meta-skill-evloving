---
name: max-best-practices
description: >
  MAX AI inference framework best practices from Modular. Use when deploying
  models with MAX Serve, building graphs with MAX Graph API, or optimizing
  inference performance. Covers multi-GPU, quantization, and production deployment.
  Supports both stable (v25.7) and nightly (v26.2).
license: MIT
compatibility: >
  Requires MAX SDK (stable v25.7 or nightly v26.1+).
  Multi-GPU requires NVIDIA Hopper+ (H100/H200/B200) or AMD MI300X.
  Container deployment requires Docker 24+ or Kubernetes 1.28+.
metadata:
  author: Modular Community
  version: "3.1.0"
  triggers:
    - Deploy MAX model
    - MAX Serve
    - max serve
    - MAX inference
    - Multi-GPU inference
    - MAX Graph
    - MAX Engine
    - MAX container
    - OpenAI-compatible endpoint
    - LLM serving
    - Model deployment
  supported_versions:
    stable: "25.7"
    nightly: "26.2"
  categories:
    - serve
    - multigpu
    - engine
    - graph
    - model
    - performance
    - deployment
globs: ["**/max.serve*", "**/max_serve*", "**/*max*.yaml", "**/*max*.yml"]
alwaysApply: false
---

<!-- AGENT UPDATE CHECK: Run `scripts/check-skill-updates.sh --json` periodically to check for updates -->
<!-- Last verified: 2026-01-26 | Remote: https://github.com/modularml/agent-skills -->

# MAX Best Practices

Best practices for the MAX AI inference framework. **13 patterns** across **7 categories**.

## Start Here: Priority Tiers

| Tier | Patterns | When to Load |
|------|----------|--------------|
| **Essential** | `serve-configuration`, `serve-kv-cache`, `serve-api`, `model-loading`, `serve-monitoring` | Always - core serving config |
| **Multi-GPU** | `multigpu-scaling` | Scaling across GPUs |
| **Production** | `deploy-deployment`, `serve-request-lifecycle` | Deployment & monitoring |
| **Advanced** | `engine-operations`, `graph-construction`, `perf-inference` | Specific use cases on demand |

## Top 10 High-Impact Patterns

| Pattern | Impact | When to Use |
|---------|--------|-------------|
| `serve-configuration` | CRITICAL | Configure `--max-batch-size`, `--max-batch-input-tokens` for throughput |
| `serve-kv-cache` | CRITICAL | Use PAGED with `--kv-cache-page-size` (multiple of 128), prefix caching |
| `multigpu-scaling` | CRITICAL | Large models across GPUs with `--devices gpu:0,1,...` |
| `engine-operations` | HIGH | Write kernels with `@compiler.register`, custom ops |
| `deploy-deployment` | HIGH | Use `modular/max-nvidia-full:latest` for production |
| `serve-api` | HIGH | Streaming, structured output, function calling, LoRA |
| `graph-construction` | HIGH | Build graphs with `Graph(TensorType(...))`, `graph.output()` |
| `serve-monitoring` | HIGH | Prometheus metrics, health endpoints |
| `engine-quantization` | HIGH | Float8, GPTQ quantization |
| `perf-inference` | HIGH | Chunked prefill, KV swapping |

## Quick Decision Tree

```
Deploy model endpoint?
  └─ serve-configuration, serve-kv-cache, serve-api

Multi-GPU inference?
  └─ multigpu-scaling
  └─ NVIDIA Hopper (H100/H200/B200)? → covered in multigpu-scaling
  └─ AMD MI300X? → covered in multigpu-scaling

Custom operations?
  └─ engine-operations + mojo gpu-fundamentals

Build custom model architecture?
  └─ engine-operations (complete project structure)
  └─ graph-construction (MAX Graph APIs)
  └─ mojo struct-design + memory-ownership (model layers)

Optimize performance?
  └─ serve-kv-cache (prefix caching), perf-inference

Production deployment?
  └─ deploy-deployment, serve-monitoring
```

## Version Support

This skill supports both **stable** and **nightly** MAX versions:

| Version | MAX | Notes |
|---------|-----|-------|
| **Stable** | v25.7 | Version-specific API in pattern files |
| **Nightly** | v26.2 | Version-specific API in pattern files |

**Detect your version:** Run `max version` or `pip show max | grep Version`

### CRITICAL: Version Alignment Check

**MAX Python package and Mojo versions MUST be aligned.** Mismatched versions cause cryptic kernel compilation failures.

**Check alignment with:**
```bash
# Quick check
mojo --version          # e.g., Mojo 0.25.7.0
pip show max | grep Version  # e.g., 25.7.0 (must match!)

# Or run the alignment checker:
./scripts/check-version-alignment.sh
# or
python scripts/check_version_alignment.py
```

**Common version mismatch errors:**
```
error: no matching function in call to 'foreach'
note: callee parameter 'func' has 'fn[width: Int, element_alignment: Int]...' type,
      but value has type 'fn[width: Int]...'
```

**How to avoid mismatches:**

1. **Always use pixi environments** - pixi manages both MAX and Mojo together:
   ```bash
   pixi shell  # ALWAYS work inside the shell
   ```

2. **Don't mix global pip installs with pixi** - if you have a global `pip install max`, it can override pixi's version

3. **Verify before debugging** - run the version check script first when encountering kernel errors

See [breaking changes](references/breaking-changes.md) for detailed API differences.

### Key API Differences

| Feature | Stable (v25.7) | Nightly (v26.2) |
|---------|----------------|-----------------|
| **foreach callback** | `fn[width: Int, element_alignment: Int](idx)` | `fn[width: Int](idx)` |
| DeviceRef | `DeviceRef.from_device(device)` | `DeviceRef.CPU()` / `DeviceRef.GPU()` |
| ops.custom() | `ops.custom(name, values, out_types)` | `ops.custom(name, device, values, out_types)` |
| TensorType | `device` optional | `device` required |
| Kernel imports | `from tensor import ...` | `from tensor import ...` |
| Driver API | `max.driver.Tensor` | `max.driver.Buffer` |
| Batch size semantics | Aggregate across replicas | Per-replica with DP |
| Prefill chunk size | `prefill_chunk_size` | `max_batch_input_tokens` |
| Max context length | `max_batch_context_length` | `max_batch_total_tokens` |
| CE batch size CLI | `--max-ce-batch-size` | Deprecated → `--max-batch-size` |
| Scheduling | Default | `--kvcache-ce-watermark` (new) |
| Llama 3.2 Vision | Supported | **Removed** |
| Gemma3 Vision | Not available | Supported (12B, 27B) |
| V1 layer classes | Deprecated | **Removed** |
| Apple silicon | `accelerator_count()` = 0 | Returns non-zero |
| Streams | Blocking option | All non-blocking |

[stable changelog](https://docs.modular.com/stable/max/changelog/) | [nightly changelog](https://docs.modular.com/max/changelog/) | [breaking changes](references/breaking-changes.md)

**Related:** [mojo-best-practices](../mojo-best-practices/SKILL.md) for Mojo language and GPU kernel development.

### Cross-Skill: Building Custom Models with Mojo

When building custom model architectures that combine Mojo layers with MAX serving:

| MAX Pattern | Mojo Pattern | Use For |
|-------------|--------------|---------|
| `engine-operations` | `struct-design` | Architecture registration + model config |
| `engine-operations` | `gpu-fundamentals` | Custom GPU kernels with @compiler.register |
| `engine-weights` | `memory-ownership` | Weight loading with UnsafePointer |
| `graph-construction` | `fn-design` | MAX Graph ops + Mojo helper functions |

See [engine-operations.md](patterns/engine-operations.md) for complete project structure example with pixi.toml and pyproject.toml setup.

## Quick Decision Guide

| Goal | Category | Key Patterns |
|------|----------|--------------|
| Deploy model endpoint | MAX Serve | `serve-configuration`, `serve-kv-cache` |
| Multi-GPU inference | Parallelism | `multigpu-scaling` |
| Build custom model | MAX Graph | `graph-construction` |
| Optimize latency | Performance | `serve-kv-cache`, `perf-inference` |
| Production deployment | Deployment | `deployment` |
| Write custom kernels | Engine + Mojo | `engine-operations` + mojo `gpu-*` patterns |
| **Build complete custom model** | **Mojo + MAX** | `engine-operations` (see project structure) |

## Pattern Categories

| Priority | Category | Count | Prefix |
|----------|----------|-------|--------|
| CRITICAL | MAX Serve Configuration | 5 | `serve-` |
| CRITICAL | Multi-GPU & Parallelism | 1 | `multigpu-` |
| HIGH | MAX Engine | 3 | `engine-` |
| HIGH | MAX Graph API | 1 | `graph-` |
| HIGH | Model Loading | 1 | `model-` |
| MEDIUM | Performance Optimization | 1 | `perf-` |
| MEDIUM | Deployment | 1 | `deploy-` |

*Version-specific API differences are documented within each pattern file.*

---

## MAX Serve (CRITICAL)

| Pattern | Description |
|---------|-------------|
| `serve-configuration` | Batch config, ragged batching, scheduling, environment |
| `serve-kv-cache` | KV cache strategy, memory management, prefix caching |
| `serve-request-lifecycle` | Request cancellation, preemption, error propagation |
| `serve-api` | Streaming, token budget, structured output, function calling, LoRA |
| `serve-monitoring` | Metrics, telemetry, health endpoints, worker lifecycle |

## Multi-GPU (CRITICAL)

| Pattern | Description |
|---------|-------------|
| `multigpu-scaling` | Tensor parallel, NVIDIA Hopper, AMD MI300, device selection |

## MAX Engine (HIGH)

| Pattern | Description |
|---------|-------------|
| `engine-weights` | Weight sharding, adapters, buffer transfer, DLPack |
| `engine-quantization` | Float8 config, GPTQ, graph quantization |
| `engine-operations` | Custom ops, architecture registration, inference sessions, subgraphs |

## MAX Graph API (HIGH)

| Pattern | Description |
|---------|-------------|
| `graph-construction` | Graph building, lazy context, modules, symbolic dims, pipelines |

## Model Loading (HIGH)

| Pattern | Description |
|---------|-------------|
| `model-loading` | Supported architectures, HuggingFace token setup |

## Performance (MEDIUM)

| Pattern | Description |
|---------|-------------|
| `perf-inference` | Chunked prefill, in-flight batching, KV swapping |

## Deployment (MEDIUM)

| Pattern | Description |
|---------|-------------|
| `deployment` | Containers, volumes, benchmarking, cloud providers (AWS/Azure/GCP), Kubernetes |

---

## Cross-References with Mojo

For GPU kernel development, see **mojo-best-practices**:
- Custom ops → `engine-operations` + mojo `gpu-fundamentals`
- GPU memory → mojo `gpu-memory-access`
- Tensor cores → mojo `gpu-tensor-cores`
- Warp primitives → mojo `gpu-warp`

## File Structure

```
skills/max-best-practices/
├── SKILL.md               # Main reference (this file)
├── AGENTS.md              # Auto-generated pattern index
├── metadata.json          # Skill metadata
├── CHANGELOG.md           # Skill version history
├── references/
│   ├── breaking-changes.md
│   └── cli-flags.md
└── patterns/              # 13 patterns with version-specific sections
    ├── serve-*.md         # MAX Serve (5)
    ├── multigpu-*.md      # Multi-GPU (1)
    ├── engine-*.md        # Engine (3)
    ├── graph-*.md         # Graph API (1)
    ├── model-*.md         # Model loading (1)
    ├── perf-*.md          # Performance (1)
    └── deploy*.md         # Deployment (1)
```

## Local Implementation Notes

When using this skill in a project, agents should collect implementation notes **locally within that project**, not globally. This ensures project-specific learnings stay with the project.

**Where to store notes:**
```
your-project/
├── IMPLEMENTATION_NOTES.md    # Project-specific learnings
├── .cursor/
│   └── rules/                 # Project-specific rules
└── ...
```

**What to capture:**
- Model-specific configuration that worked
- Performance tuning for your hardware (GPU type, memory)
- Batch size optimizations for your workload
- Deployment configuration decisions
- Integration patterns with your infrastructure

**Usage:** Agents should check for and update `IMPLEMENTATION_NOTES.md` in the project root when discovering new patterns or resolving issues.

## Updating This Skill

When the user asks to "update this skill" or "get the latest version", follow these steps:

**1. Determine the skill's install location:**
```bash
# The skill is typically installed at one of these locations:
# - ~/.claude/skills/max-best-practices (Claude Code default)
# - Custom path specified during installation
```

**2. Check for updates:**
```bash
# From the skill's parent directory (e.g., ~/.claude/skills or the agent-skills repo)
./scripts/check-skill-updates.sh --json
```

**3. Update the skill:**
```bash
# If installed via git clone (recommended):
cd <skill-parent-directory>  # e.g., ~/.claude/skills or ~/github/agent-skills
git pull origin main

# If installed via install.sh:
./install.sh --update
```

**4. Verify the update:**
- Read `metadata.json` to confirm the new version and `last_verified` date
- Check that patterns match the user's MAX version (`max version`)

**Repository:** https://github.com/modularml/agent-skills

**Note:** Skills are updated frequently to track Mojo/MAX nightly releases. The `last_verified` date in `metadata.json` indicates when patterns were last validated against the changelog.

## Navigation

- **Installation?** See [references/installation.md](references/installation.md) (pixi, uv, pip, conda)
- **CLI flags?** See [references/cli-flags.md](references/cli-flags.md)
- **Breaking changes?** See [references/breaking-changes.md](references/breaking-changes.md)
- **Full pattern index?** See [AGENTS.md](AGENTS.md)
- **Mojo/GPU kernels?** See [mojo-best-practices](../mojo-best-practices/SKILL.md)
