# Mojo Best Practices Skill

A comprehensive best practices guide for Mojo programming, designed for AI agents and LLMs.

## Overview

This skill provides **25 patterns across 12 categories** for writing safe, performant, and idiomatic Mojo code. Patterns are organized by priority tiers and deliver significant performance gains (10x-17,000x vs Python depending on optimization level). Version-specific features are documented within each pattern file.

**Version:** 5.1.0 | **Last Verified:** 2026-01-26

## Quick Start for Agents

**Start with [SKILL.md](SKILL.md)** - the main reference with priority tiers, decision trees, and pattern categories.

### Priority Tier System

| Tier | Focus | Load When |
|------|-------|-----------|
| **Essential** | Memory safety, ownership, basic types | Always - covers 80% of use cases |
| **Performance** | SIMD vectorization, parallelization, BLAS | Optimizing CPU-bound code |
| **GPU** | Tensor cores, TMA, synchronization | Any GPU kernel development |
| **Advanced** | Metaprogramming, edge cases | Specific scenarios on demand |

## Version Support

This skill supports **both stable and nightly** versions of Mojo:

| Version | Mojo | Notes |
|---------|------|-------|
| **Stable** | v25.7 | Version-specific syntax in "Version-Specific Features" sections |
| **Nightly** | v0.26.2 | Version-specific syntax in "Version-Specific Features" sections |

**How version support works:**
- Each pattern file contains a "Version-Specific Features" section
- The `SKILL.md` and `references/breaking-changes.md` document all differences

**Detect your version:**
```bash
mojo --version           # Direct check
pixi list | grep mojo    # In pixi environment
```

**Install Mojo:** See [references/installation.md](references/installation.md) for complete instructions.

```bash
# Quick install (pixi)
pixi add mojo              # Nightly
pixi add "mojo==0.25.7"    # Stable
```

**Key differences between stable and nightly:**

| Feature | Stable (v25.7) | Nightly (v0.26.1+) |
|---------|----------------|-------------------|
| Constants | `alias` | `comptime` (preferred) |
| Struct alignment | Not available | `@align(N)` decorator |
| Typed errors | Not available | `fn foo() raises CustomError` |
| Never type | Not available | `fn abort() -> Never` |
| Compile-time expr | Implicit | `comptime(expr)` explicit |
| Copyable trait | `Copyable, Movable` | `Copyable` refines `Movable` |

**Changelogs:**
- [Stable changelog](https://docs.modular.com/stable/mojo/changelog)
- [Nightly changelog](https://docs.modular.com/mojo/changelog/)

## Categories

| Priority | Category | Patterns | Focus |
|----------|----------|----------|-------|
| CRITICAL | Memory Safety & Ownership | 3 | Ownership, origins, ref counting |
| CRITICAL | Type System | 3 | Compile-time safety, SIMD, traits |
| CRITICAL | GPU Programming | 7 | SM90/SM100 tensor cores, TMA, warp specialization |
| CRITICAL | C Interoperability (FFI) | 1 | BLAS/Accelerate, vendor libraries |
| HIGH | Struct Design | 1 | @fieldwise_init, ergonomics |
| HIGH | Function Design | 1 | API clarity, performance |
| HIGH | Testing | 1 | Test suites, benchmarks |
| HIGH | Debugging | 1 | Numerical accuracy, GPU debugging |
| MEDIUM-HIGH | Error Handling | 1 | Typed raises, debugging |
| MEDIUM | Performance Optimization | 4 | SIMD, parallelization, kernel fusion |
| MEDIUM | Python Interoperability | 1 | Integration, migration |
| LOW | Advanced Metaprogramming | 1 | comptime, code generation |

**Total: 25 patterns** (version-specific content is within each pattern)

## Directory Structure

```
mojo-best-practices/
├── SKILL.md              # Main reference (START HERE)
├── AGENTS.md             # Complete index with all code examples
├── README.md             # This file
├── metadata.json         # Skill metadata
├── ERROR_INDEX.md        # Error message to pattern mapping
├── SCENARIOS.md          # Task/scenario to pattern mapping
├── references/
│   └── breaking-changes.md  # Version compatibility guide
├── scripts/
│   └── build_agents.py   # Regenerate AGENTS.md
└── patterns/             # 25 patterns with version-specific sections
    ├── memory-*.md       # Memory safety (3)
    ├── type-*.md         # Type system (3)
    ├── gpu-*.md          # GPU programming (7)
    ├── ffi-*.md          # C interoperability (1)
    ├── struct-*.md       # Struct design (1)
    ├── fn-*.md           # Function design (1)
    ├── test*.md          # Testing (1)
    ├── debug*.md         # Debugging (1)
    ├── error-*.md        # Error handling (1)
    ├── perf-*.md         # Performance (4)
    ├── python-*.md       # Python interop (1)
    └── meta-*.md         # Metaprogramming (1)
```

## Usage

### Recommended Flow for AI Agents

1. **[SKILL.md](SKILL.md)** - Start here. Priority tiers, decision trees, and pattern summaries.

2. **Specific patterns on demand** - Load individual `patterns/*.md` files based on the task. Essential tier patterns cover 80% of use cases.

3. **[ERROR_INDEX.md](ERROR_INDEX.md)** - When encountering errors, look up patterns by error message.

4. **[AGENTS.md](AGENTS.md)** - Complete index with all 25 patterns and code examples. Use for comprehensive context.

### When to Use This Skill

- Writing new Mojo code
- Reviewing or refactoring existing code
- Converting Python to Mojo (10x-17,000x speedup potential)
- GPU kernel development
- Performance optimization

### Key Patterns by Scenario

**Starting a new Mojo project:**
- `memory-ownership` - Implement proper constructors/destructors
- `struct-design` - Use @fieldwise_init for automatic initialization
- `type-traits` - Use Self.T for generic parameters

**Optimizing performance:**
- `perf-vectorization` - SIMD parallelism (4-16x speedup)
- `perf-parallelization` - Multi-core execution (near-linear scaling)
- `ffi-interop` - Apple BLAS for matmul (25-32x speedup)
- `perf-memory` - Hide latency with parallel accumulators

**GPU acceleration:**
- `gpu-fundamentals` - Thread hierarchy, DeviceContext, kernel launch
- `gpu-memory-access` - Coalesced memory access patterns
- `gpu-tensor-cores` - Hopper/Blackwell tensor core patterns

**Migrating from Python:**
- `python-interop` - Convert at boundaries (10-100x speedup)
- `fn-design` - Choose appropriate function style

## Installation

Install Mojo:

```bash
# Stable (using pixi)
pixi add max

# Nightly (using pixi)
pixi add max --channel https://conda.modular.com/nightly

# Verify installation
mojo --version
```

## Contributing

**Design Principle: Patterns should be comprehensive, not fragmented.**

### Prefer Updating Over Creating

Before creating a new pattern:
1. Search existing patterns for related content
2. Check if your content fits in an existing pattern
3. Only create new if the topic is genuinely distinct

### When to Update vs Create

| Situation | Action |
|-----------|--------|
| New technique for existing topic | Update existing pattern |
| Fix or expand existing content | Update existing pattern |
| Genuinely new topic | Create new pattern |
| Would make pattern >1500 lines | Consider splitting |

### Adding or Updating a Pattern

1. **Read existing patterns first** in `patterns/`
2. **Update or create** following `patterns/_template.md`
3. **Name correctly**: Must match category prefix (`memory-*`, `gpu-*`, etc.)
4. **Test code**: All examples must compile with `mojo run`
5. **Validate**: `python scripts/validate-patterns.py`
6. **Regenerate**: `python scripts/build_agents.py`
7. **Verify counts**: `python scripts/validate-counts.py` (from repo root)

### File Locations

All patterns are in `patterns/`. Version-specific syntax is documented within each pattern's "Version-Specific Features" section.

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for full guidelines.

## References

- [Mojo Manual](https://docs.modular.com/mojo/manual/)
- [Mojo Standard Library](https://docs.modular.com/mojo/std/)
- [Mojo Stable Changelog](https://docs.modular.com/stable/mojo/changelog)
- [Mojo Nightly Changelog](https://docs.modular.com/mojo/changelog/)
- [MAX Kernels (GPU examples)](https://github.com/modular/modular/tree/main/max/kernels)

## License

MIT
