---
name: mojo-best-practices
description: >
  Mojo programming best practices from the official modular/modular repository.
  Use when writing, reviewing, or optimizing Mojo code. Covers memory safety,
  ownership patterns, GPU kernels (SM90/SM100 tensor cores), BLAS integration,
  testing patterns, and performance optimization. Supports both stable (v25.7)
  and nightly (v0.26.2).
license: MIT
compatibility: >
  Requires Mojo SDK (stable v25.7 or nightly v0.26.1+).
  GPU patterns require NVIDIA CUDA 12+ or AMD ROCm 6+.
  Apple Metal patterns require macOS 14+ with Apple Silicon.
metadata:
  author: Modular Community
  version: "5.1.0"
  triggers:
    - Write Mojo code
    - Convert Python to Mojo
    - Optimize Mojo function
    - Review Mojo code
    - Write GPU kernel in Mojo
    - Use BLAS in Mojo
    - Mojo memory safety
    - Mojo ownership
  supported_versions:
    stable: "25.7"
    nightly: "0.26.2"
  categories:
    - memory-safety
    - type-system
    - gpu-programming
    - c-interoperability
    - struct-design
    - function-design
    - testing
    - debugging
    - error-handling
    - performance
    - python-interop
    - metaprogramming
globs: ["**/*.mojo", "**/*.🔥"]
alwaysApply: false
---

<!-- AGENT UPDATE CHECK: Run `scripts/check-skill-updates.sh --json` periodically to check for updates -->
<!-- Last verified: 2026-01-26 | Remote: https://github.com/modularml/agent-skills -->

# Mojo Best Practices

Best practices for Mojo programming. **25 patterns** across **12 categories**.

## Start Here: Priority Tiers

| Tier | Patterns | Load When |
|------|----------|-----------|
| **Essential** | `memory-ownership`, `memory-safety`, `type-system`, `struct-design`, `fn-design`, `error-handling` | Always load first - covers 80% of use cases |
| **Performance** | `perf-vectorization`, `perf-parallelization`, `perf-memory`, `ffi-interop` | Optimizing CPU performance |
| **GPU** | `gpu-fundamentals`, `gpu-synchronization`, `gpu-tensor-cores`, `gpu-memory-access`, `gpu-kernels` | Any GPU kernel work |
| **Advanced** | Remaining patterns in `patterns/` | Specific edge cases on demand |

## Top 10 High-Impact Patterns

| Pattern | Impact | When to Use |
|---------|--------|-------------|
| `perf-parallelization` | 10x-17,000x vs Python* | CPU-bound loops, multi-core |
| `perf-vectorization` | 4-16x | Numeric computations, SIMD |
| `gpu-fundamentals` | 10-100x | Any GPU kernel development |
| `ffi-interop` | 25-32x | Matrix ops on Apple Silicon (BLAS) |
| `memory-ownership` | Safety | Use `^` for ownership, avoid use-after-free |
| `gpu-tensor-cores` | 10-100x | H100/H200/B200 matmuls |
| `type-simd` | 4-16x | SIMD[DType, width] for numerics |
| `perf-memory` | 1.5-2x | Hide latency with accumulators, alignment |
| `memory-safety` | Safety | Safe pointers, origin tracking |
| `struct-design` | Productivity | Use `@fieldwise_init` for simple structs |

*\*Ranges: 10x for simple typed code, 17,000x for vectorized+parallelized hot paths. Benchmark your use case.*

## Quick Decision Tree

```
GPU code?
  Yes --> gpu-fundamentals
          SM90 (H100)? --> gpu-tensor-cores
          SM100 (B200)? --> gpu-tensor-cores
          TMA? --> gpu-memory-access
          AMD? --> gpu-amd

Performance critical?
  Yes --> perf-vectorization (SIMD), perf-parallelization (multi-core)
          Apple Silicon? --> ffi-interop (BLAS 25-32x)

Memory error?
  "use of moved value" --> memory-ownership
  Use-after-free --> memory-safety, memory-ownership
  Memory leak --> memory-ownership
  Origin/lifetime --> memory-safety

Struct design?
  Simple data --> struct-design (uses @fieldwise_init)
  Custom lifecycle --> memory-ownership
  Traits --> type-traits
```

## Version Support

This skill supports both **stable** and **nightly** Mojo versions:

| Version | Mojo | Notes |
|---------|------|-------|
| **Stable** | v25.7 | Version-specific syntax in pattern files |
| **Nightly** | v0.26.2 | Version-specific syntax in pattern files |

**Detect your version:** Run `mojo --version` or check `pixi list | grep mojo`

**Key differences:** Most breaking changes are now in **both** versions. Nightly-only features:

| Feature | Stable (v25.7) | Nightly (v0.26.2+) |
|---------|----------------|-------------------|
| Constants | `alias` | `comptime` (preferred, `alias` deprecated) |
| Struct alignment | Not available | `@align(N)` decorator |
| Typed errors | Not available | `fn foo() raises CustomError` |
| Never type | Not available | `fn abort() -> Never` |
| Compile-time expr | Implicit | `comptime(expr)` explicit |
| Trait methods | `pass` only | `...` (no default) vs `pass` (empty) |
| Fn type conversion | Explicit | Non-raising → raising implicit |
| Copyable trait | `Copyable, Movable` | `Copyable` refines `Movable` |
| Struct reflection | Not available | `struct_field_count[T]()` |
| Linear types | `AnyType` needs `__del__()` | `ImplicitlyDestructible` trait |

**Shared syntax (v25.7+):**
- `@fieldwise_init` (not `@value`)
- `var`/`deinit` (not `owned`)
- `Writable` trait (not `Stringable`)

[stable changelog](https://docs.modular.com/stable/mojo/changelog) | [nightly changelog](https://docs.modular.com/mojo/changelog/) | [breaking changes](references/breaking-changes.md)

**Related:** [max-best-practices](../max-best-practices/SKILL.md) for MAX Serve deployment and inference.

### Cross-Skill: Building Custom Models

When building complete model architectures that combine Mojo layers with MAX serving:

| Mojo Pattern | MAX Pattern | Use For |
|--------------|-------------|---------|
| `struct-design` | `engine-operations` | Model config and architecture registration |
| `memory-ownership` | `engine-weights` | Weight matrices with UnsafePointer |
| `gpu-fundamentals` | `engine-operations` | Custom GPU kernels with @compiler.register |

See [max-best-practices/engine-operations.md](../max-best-practices/patterns/engine-operations.md) for complete project structure example.

## Quick Decision Guide

| Goal | Category | Key Patterns |
|------|----------|--------------|
| Write safe code | Memory Safety | `memory-ownership`, `memory-safety` |
| Maximum performance | Performance | `perf-vectorization`, `perf-parallelization` (10x-17,000x vs Python) |
| GPU acceleration | GPU Programming | `gpu-fundamentals`, `gpu-tensor-cores` |
| BLAS acceleration | C Interop | `ffi-interop` (25-32x speedup) |
| Migrate from Python | Python Interop | `python-interop` |
| Design APIs | Struct + Function | `struct-design`, `fn-design` |
| **Build custom model** | **Mojo + MAX** | `struct-design`, `memory-ownership` + MAX `engine-operations` |

## Pattern Categories

| Priority | Category | Count | Prefix |
|----------|----------|-------|--------|
| CRITICAL | Memory Safety & Ownership | 3 | `memory-` |
| CRITICAL | Type System | 3 | `type-` |
| CRITICAL | GPU Programming | 7 | `gpu-` |
| CRITICAL | C Interoperability | 1 | `ffi-` |
| HIGH | Struct Design | 1 | `struct-` |
| HIGH | Function Design | 1 | `fn-` |
| HIGH | Testing | 1 | `test-` |
| HIGH | Debugging | 1 | `debug-` |
| MEDIUM-HIGH | Error Handling | 1 | `error-` |
| MEDIUM | Performance Optimization | 4 | `perf-` |
| MEDIUM | Python Interoperability | 1 | `python-` |
| LOW | Advanced Metaprogramming | 1 | `meta-` |

*Version-specific features are documented within each pattern file.*

---

## Debugging Memory Issues

If you're experiencing memory errors, use this decision tree to find the relevant patterns:

| Symptom | Likely Cause | Key Patterns |
|---------|--------------|--------------|
| "use of moved value" | Missing ownership transfer | `memory-ownership` |
| Use-after-free | Object destroyed too early | `memory-safety`, `memory-ownership` |
| Memory leak | Missing destructor call | `memory-ownership`, `memory-safety` |
| Double-free | Duplicate destruction | `memory-safety` |
| GPU OOM | Buffer not released | `gpu-fundamentals`, `perf-memory` |
| Crash in loop | Reference invalidation | `memory-safety` |
| "does not implement Copyable" | Missing trait | `type-traits`, `struct-design` |

**See Also:** `debugging` for GPU memory issues, `error-handling` for automatic cleanup.

## Memory Safety (CRITICAL)

| Pattern | Description |
|---------|-------------|
| `memory-ownership` | Ownership transfer with `^`, borrow vs copy, lifecycle methods |
| `memory-safety` | Dangling references, origin tracking, safe pointers, Span usage |
| `memory-refcounting` | Reference counting implementation, atomic operations |

## Type System (CRITICAL)

| Pattern | Description |
|---------|-------------|
| `type-system` | Explicit annotations, optional types, numeric precision |
| `type-simd` | SIMD vectorization, register-passable types |
| `type-traits` | Parametric traits, trait composition, conditional conformance |

## GPU Programming (CRITICAL)

| Pattern | Description |
|---------|-------------|
| `gpu-fundamentals` | Thread hierarchy, memory coalescing, shared memory |
| `gpu-synchronization` | Barriers, async transactions, async copy |
| `gpu-tensor-cores` | SM90/SM100 patterns, WGMMA, TCGen05 |
| `gpu-memory-access` | TMA loading, prefetch, swizzle patterns |
| `gpu-warp` | Warp primitives, specialization, reduction |
| `gpu-kernels` | Kernel fusion, pipelines, double-buffering |
| `gpu-amd` | AMD MFMA shapes, scheduling, waitcnt |

## C Interoperability (CRITICAL)

| Pattern | Description |
|---------|-------------|
| `ffi-interop` | CString safety, libc functions, Apple BLAS (25-32x speedup) |

## Performance (MEDIUM)

| Pattern | Description |
|---------|-------------|
| `perf-vectorization` | `vectorize` function (4-16x SIMD speedup) |
| `perf-parallelization` | `parallelize` + SIMD (10x-17,000x vs Python*) |
| `perf-memory` | Alignment, layout, prefetch, stack vs heap |
| `perf-optimization` | Caching, lazy loading, multiple accumulators |

## Testing (HIGH)

| Pattern | Description |
|---------|-------------|
| `testing` | Test suites, benchmarks, quickbench patterns |

*\*Performance ranges: Lower bound = simple typed loops vs Python. Upper bound = fully vectorized + parallelized hot paths. Actual gains depend on workload, data size, and hardware. Always benchmark your specific use case.*

---

## File Structure

```
skills/mojo-best-practices/
├── SKILL.md               # Main reference (this file)
├── AGENTS.md              # Auto-generated pattern index
├── metadata.json          # Skill metadata
├── CHANGELOG.md           # Skill version history
├── references/            # Detailed reference docs
│   ├── breaking-changes.md
│   └── apple-metal/       # macOS-specific Metal/MPS patterns (8 files)
└── patterns/              # 25 patterns with version-specific sections
    ├── memory-*.md        # Memory safety (3 patterns)
    ├── gpu-*.md           # GPU programming (7 patterns)
    ├── type-*.md          # Type system (3 patterns)
    ├── perf-*.md          # Performance (4 patterns)
    └── _template.md       # Template for new patterns
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
- Version-specific workarounds discovered
- Performance optimizations that worked for this codebase
- API quirks encountered
- Build configuration decisions
- Platform-specific adjustments (macOS/Linux/GPU)

**Usage:** Agents should check for and update `IMPLEMENTATION_NOTES.md` in the project root when discovering new patterns or resolving issues.

## Updating This Skill

When the user asks to "update this skill" or "get the latest version", follow these steps:

**1. Determine the skill's install location:**
```bash
# The skill is typically installed at one of these locations:
# - ~/.claude/skills/mojo-best-practices (Claude Code default)
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
- Check that patterns match the user's Mojo version (`mojo --version`)

**Repository:** https://github.com/modularml/agent-skills

**Note:** Skills are updated frequently to track Mojo/MAX nightly releases. The `last_verified` date in `metadata.json` indicates when patterns were last validated against the changelog.

## Navigation

- **Installation?** See [references/installation.md](references/installation.md) (pixi, uv, pip, conda)
- **Need a specific pattern?** Check `patterns/` directory
- **Breaking changes?** See [references/breaking-changes.md](references/breaking-changes.md)
- **Full pattern index?** See [AGENTS.md](AGENTS.md)
