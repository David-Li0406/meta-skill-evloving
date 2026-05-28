# MAX Best Practices Skill

A comprehensive best practices guide for the MAX AI inference framework, designed for AI agents and LLMs.

## Overview

This skill provides **13 patterns across 7 categories** for deploying, configuring, and optimizing MAX AI inference. Patterns are organized by priority tiers from Essential (core serving) to Advanced (specific use cases). Version-specific API differences are documented within each pattern file.

**Version:** 3.1.0 | **Last Verified:** 2026-01-26

## Quick Start for Agents

**Recommended reading order:**

1. **[SKILL.md](SKILL.md)** - Start here. Priority tiers, top 10 patterns, decision tree
2. **[patterns/](patterns/)** - Load specific patterns on demand based on task
3. **[ERROR_INDEX.md](ERROR_INDEX.md)** - When encountering errors, look up patterns by error message
4. **[AGENTS.md](AGENTS.md)** - Complete index with all code examples

## Priority Tiers

| Tier | Patterns | When to Load |
|------|----------|--------------|
| **Essential** | `serve-configuration`, `serve-kv-cache`, `serve-api`, `model-loading`, `serve-monitoring` | Always - core serving config |
| **Multi-GPU** | `multigpu-scaling` | Scaling across GPUs |
| **Production** | `deployment`, `serve-request-lifecycle` | Deployment & monitoring |
| **Advanced** | `engine-operations`, `graph-construction`, `perf-inference` | Specific use cases on demand |

## Version Support

This skill supports **both stable and nightly** versions of MAX:

| Version | MAX | Notes |
|---------|-----|-------|
| **Stable** | v25.7 | Version-specific API in "Version-Specific Features" sections |
| **Nightly** | v26.2 | Version-specific API in "Version-Specific Features" sections |

**Detect your version:**
```bash
max version              # Direct check
pixi list | grep modular # In pixi environment
```

**Install MAX:** See [references/installation.md](references/installation.md) for complete instructions.

```bash
# Quick install (pixi)
pixi add modular              # Nightly
pixi add "modular==25.7"      # Stable
```

**Key differences:**

| Feature | Stable (v25.7) | Nightly (v26.1) |
|---------|----------------|-----------------|
| Batch size semantics | Aggregate across replicas | Per-replica with DP |
| Driver API | `max.driver.Tensor` | `max.driver.Buffer` |
| Prefill config | `prefill_chunk_size` | `max_batch_input_tokens` |
| Context length | `max_batch_context_length` | `max_batch_total_tokens` |

## Categories

| Priority | Category | Patterns | Focus |
|----------|----------|----------|-------|
| CRITICAL | MAX Serve Configuration | 5 | Batch config, KV cache, LoRA, token budget, error handling |
| CRITICAL | Multi-GPU & Parallelism | 1 | Tensor/data parallelism, NVIDIA Hopper, AMD MI300 |
| HIGH | MAX Engine | 3 | Custom ops, quantization, weight adapters |
| HIGH | MAX Graph API | 1 | Graph construction, modules, symbolic dimensions |
| HIGH | Model Loading | 1 | Architectures, HuggingFace tokens |
| MEDIUM | Performance Optimization | 1 | Prefix caching, chunked prefill |
| MEDIUM | Deployment | 1 | Containers, Kubernetes, benchmarking |

**Total: 13 patterns** (version-specific content is within each pattern)

## Directory Structure

```
max-best-practices/
├── SKILL.md              # Main reference (START HERE)
├── AGENTS.md             # Complete documentation with all code examples
├── README.md             # This file
├── CHANGELOG.md          # Skill version history
├── metadata.json         # Skill metadata and references
├── ERROR_INDEX.md        # Error message to pattern mapping
├── SCENARIOS.md          # Task/scenario to pattern mapping
├── references/
│   ├── breaking-changes.md  # Version compatibility guide
│   └── cli-flags.md         # CLI flag reference
├── scripts/
│   └── build_agents.py   # Regenerate AGENTS.md
└── patterns/             # 13 patterns with version-specific sections
    ├── serve-*.md        # MAX Serve (5)
    ├── multigpu-*.md     # Multi-GPU (1)
    ├── engine-*.md       # MAX Engine (3)
    ├── graph-*.md        # MAX Graph API (1)
    ├── model-*.md        # Model loading (1)
    ├── perf-*.md         # Performance (1)
    └── deploy*.md        # Deployment (1)
```

## Contributing

**Design Principle: Patterns should be comprehensive, not fragmented.**

### Prefer Updating Over Creating

Before creating a new pattern:
1. Search existing patterns for related content
2. Check if your content fits in an existing pattern
3. Only create new if the topic is genuinely distinct

### Adding or Updating a Pattern

1. **Read existing patterns first** in `patterns/`
2. **Update or create** following `patterns/_template.md`
3. **Name correctly**: Must match category prefix (`serve-*`, `engine-*`, etc.)
4. **Validate**: `python scripts/validate-patterns.py` (from repo root)
5. **Regenerate**: `python scripts/build_agents.py`
6. **Verify counts**: `python scripts/validate-counts.py` (from repo root)

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for full guidelines.

## Maintenance

**CI scripts** (in repo root `scripts/`):
- `check-links.py` - Validates all internal and external links
- `check-api-staleness.py` - Detects outdated API references

**Regenerate AGENTS.md:**
```bash
python scripts/build_agents.py
```

## Cross-References with Mojo

For GPU kernel development, see **mojo-best-practices**:
- Custom ops → `engine-operations` + mojo `gpu-fundamentals`
- GPU memory → mojo `gpu-memory-access`
- Tensor cores → mojo `gpu-tensor-cores`

## References

- [MAX Documentation](https://docs.modular.com/max/)
- [MAX Stable Changelog](https://docs.modular.com/stable/max/changelog/)
- [MAX Nightly Changelog](https://docs.modular.com/max/changelog/)
- [MAX Container](https://docs.modular.com/max/container/)
- [MAX GitHub](https://github.com/modular/modular/tree/main/max)

## License

MIT
