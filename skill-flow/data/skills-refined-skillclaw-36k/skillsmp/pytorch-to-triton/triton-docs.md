# Triton Documentation Cache

This document provides instructions for fetching and caching Triton documentation locally.

## Directory Structure

Documentation is cached in `docs/.triton_docs/` at the repository root:

```
docs/
└── .triton_docs/
    ├── README.md              # Index of cached docs
    ├── language-reference.md  # Core Triton language guide
    ├── tutorials/
    │   ├── 01-vector-add.md
    │   ├── 02-fused-softmax.md
    │   ├── 03-matmul.md
    │   └── 04-low-memory-dropout.md
    └── best-practices.md      # Optimization patterns
```

## Fetching Documentation

### Step 1: Create the directory

```bash
mkdir -p docs/.triton_docs/tutorials
```

### Step 2: Fetch documentation using WebFetch

Use Claude's WebFetch tool to download and extract documentation from these URLs:

#### Core Language Reference
```
URL: https://triton-lang.org/main/python-api/triton.language.html
Prompt: Extract the complete Triton language reference documentation including all functions, their signatures, descriptions, and examples. Format as markdown.
Save to: docs/.triton_docs/language-reference.md
```

#### Vector Add Tutorial
```
URL: https://triton-lang.org/main/getting-started/tutorials/01-vector-add.html
Prompt: Extract the complete vector addition tutorial including all code examples, explanations of program IDs, block sizes, and memory access patterns. Format as markdown.
Save to: docs/.triton_docs/tutorials/01-vector-add.md
```

#### Fused Softmax Tutorial
```
URL: https://triton-lang.org/main/getting-started/tutorials/02-fused-softmax.html
Prompt: Extract the complete fused softmax tutorial including the naive and optimized implementations, reduction patterns, and numerical stability techniques. Format as markdown.
Save to: docs/.triton_docs/tutorials/02-fused-softmax.md
```

#### Matrix Multiplication Tutorial
```
URL: https://triton-lang.org/main/getting-started/tutorials/03-matrix-multiplication.html
Prompt: Extract the complete matrix multiplication tutorial including blocking strategies, autotuning, and memory hierarchy optimization. Format as markdown.
Save to: docs/.triton_docs/tutorials/03-matmul.md
```

#### Low Memory Dropout Tutorial
```
URL: https://triton-lang.org/main/getting-started/tutorials/04-low-memory-dropout.html
Prompt: Extract the complete low-memory dropout tutorial including seeded PRNG and memory-efficient patterns. Format as markdown.
Save to: docs/.triton_docs/tutorials/04-low-memory-dropout.md
```

### Step 3: Create index file

After fetching, create `docs/.triton_docs/README.md`:

```markdown
# Triton Documentation Cache

Local cache of Triton documentation for PyTorch-to-Triton conversions.

## Contents

- [Language Reference](language-reference.md) - Complete API reference
- **Tutorials**:
  - [01 - Vector Add](tutorials/01-vector-add.md) - Basics of Triton kernels
  - [02 - Fused Softmax](tutorials/02-fused-softmax.md) - Reductions and numerical stability
  - [03 - Matrix Multiplication](tutorials/03-matmul.md) - Blocking and autotuning
  - [04 - Low Memory Dropout](tutorials/04-low-memory-dropout.md) - Memory-efficient patterns
- [Best Practices](best-practices.md) - Optimization patterns

## Source

Fetched from https://triton-lang.org/main/
```

## Key Documentation Sections

### Language Primitives (from language-reference.md)

Essential functions to understand:

| Function | Purpose |
|----------|---------|
| `tl.program_id(axis)` | Get program (block) index |
| `tl.arange(start, end)` | Create index range (must be power-of-2 size) |
| `tl.load(ptr, mask, other)` | Load from memory with masking |
| `tl.store(ptr, value, mask)` | Store to memory with masking |
| `tl.zeros(shape, dtype)` | Create zero tensor |
| `tl.full(shape, value, dtype)` | Create constant tensor |
| `tl.where(cond, x, y)` | Conditional select |
| `tl.sum(x, axis)` | Sum reduction |
| `tl.max(x, axis)` | Max reduction |
| `tl.exp(x)` | Element-wise exp |
| `tl.log(x)` | Element-wise log |
| `tl.dot(a, b)` | Matrix multiplication |
| `tl.atomic_add(ptr, val)` | Atomic addition |

### Decorators

| Decorator | Purpose |
|-----------|---------|
| `@triton.jit` | JIT compile function as Triton kernel |
| `@triton.autotune` | Auto-select best config from options |
| `tl.constexpr` | Compile-time constant parameter |

### Memory Hierarchy

Understanding for optimization:

1. **Registers** - Fastest, limited per thread
2. **Shared Memory (SRAM)** - Fast, shared within block (~48-164KB)
3. **L1 Cache** - Per-SM, ~128KB
4. **L2 Cache** - Shared across SMs, ~40MB
5. **Global Memory (HBM)** - Slowest, largest

### Common Patterns

#### Reduction (from softmax tutorial)
```python
# Numerically stable reduction
max_val = tl.max(x, axis=0)
x_shifted = x - max_val
exp_x = tl.exp(x_shifted)
sum_exp = tl.sum(exp_x, axis=0)
result = x_shifted - tl.log(sum_exp)
```

#### Tiled Matrix Multiply (from matmul tutorial)
```python
# Iterate over K dimension in tiles
for k in range(0, K, BLOCK_K):
    a_tile = tl.load(a_ptr + ...)  # [BLOCK_M, BLOCK_K]
    b_tile = tl.load(b_ptr + ...)  # [BLOCK_K, BLOCK_N]
    acc += tl.dot(a_tile, b_tile)  # Accumulate in registers
```

#### Autotuning
```python
@triton.autotune(
    configs=[
        triton.Config({'BLOCK_M': 64, 'BLOCK_N': 64, 'BLOCK_K': 32}, num_warps=4),
        triton.Config({'BLOCK_M': 128, 'BLOCK_N': 64, 'BLOCK_K': 32}, num_warps=4),
        triton.Config({'BLOCK_M': 64, 'BLOCK_N': 128, 'BLOCK_K': 32}, num_warps=4),
    ],
    key=['M', 'N', 'K'],  # Retune when these change
)
@triton.jit
def kernel(...):
    ...
```

## Checking Cache Status

Before starting a conversion, verify docs are cached:

```python
import os

docs_dir = "docs/.triton_docs"
required_files = [
    "language-reference.md",
    "tutorials/01-vector-add.md",
    "tutorials/02-fused-softmax.md",
]

missing = [f for f in required_files if not os.path.exists(os.path.join(docs_dir, f))]
if missing:
    print(f"Missing documentation: {missing}")
    print("Please fetch using WebFetch tool")
else:
    print("Documentation cache is complete")
```

## Updating Documentation

Triton documentation may update. To refresh:

1. Delete `docs/.triton_docs/`
2. Re-fetch using the WebFetch instructions above
3. Verify content is complete

## Git Configuration

The `.triton_docs` directory uses a dot prefix to indicate it's a cache/generated directory. Consider adding to `.gitignore` if you don't want to commit it:

```gitignore
# Triton documentation cache (can be regenerated)
docs/.triton_docs/
```

Or commit it for offline access and faster skill execution.
