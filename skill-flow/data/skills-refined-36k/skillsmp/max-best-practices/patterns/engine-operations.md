---
title: MAX Engine Operations
description: Custom operations, architecture registration, inference sessions, and graph management
impact: HIGH
category: engine
tags: custom-ops, architecture, inference, caching, subgraphs
error_patterns:
  - "DeviceRef has no attribute 'from_device'"
  - "custom() missing required argument 'device'"
  - "TensorType missing required argument 'device'"
  - "Could not find mojo kernel"
  - "unable to locate module 'max'"
  - "Failed to resolve module path for MOGGKernelAPI"
  - "kernel compilation failed"
scenarios:
  - "Create custom MAX operation"
  - "Register new model architecture"
  - "Fix custom ops API error"
  - "Configure inference session"
  - "Run offline batch inference"
  - "Build complete custom model with MAX"
  - "Integrate Mojo layers with Python serving"
  - "Create mixed Mojo/Python model project"
consolidates:
  - engine-custom-ops.md
  - engine-custom-op-integration.md
  - engine-architecture-registration.md
  - engine-inference-session.md
  - engine-offline-inference.md
  - engine-graph-caching.md
  - engine-subgraphs.md
---

# MAX Engine Operations

**Category:** engine | **Impact:** HIGH

Comprehensive patterns for MAX Engine operations including custom operations with Mojo kernels, architecture registration for custom models, inference session management, offline batch inference, graph caching, and subgraph execution.

---

## Core Concepts

### Custom Operations with InputTensor/OutputTensor

Use `InputTensor` and `OutputTensor` types for custom ops (not deprecated `ManagedTensorSlice`).

**Critical: Version Alignment**

MAX Python package and Mojo must be version-aligned. Check with:
```bash
pip show max | grep Version   # e.g., 26.2.0
mojo --version                # Must match major.minor
```

**Pattern (Stable v25.7):**

```mojo
# kernels/my_op.mojo
import compiler
from runtime.asyncrt import DeviceContextPtr
from tensor import InputTensor, OutputTensor, foreach
from utils.index import IndexList

@compiler.register("my_op")
struct MyOp:
    @staticmethod
    fn execute[target: StaticString](
        out: OutputTensor,
        inp: InputTensor[dtype=out.dtype, rank=out.rank],
        ctx: DeviceContextPtr,
    ) raises:
        @parameter
        @always_inline
        fn op[width: Int, element_alignment: Int](idx: IndexList[out.rank]) -> SIMD[out.dtype, width]:
            return inp.load[width](idx) * 2

        foreach[op, target=target](out, ctx)
```

**Pattern (Nightly v26.2+):**

```mojo
# kernels/my_op.mojo
import compiler
from runtime.asyncrt import DeviceContextPtr
from tensor import InputTensor, OutputTensor, foreach
from utils.index import IndexList

@compiler.register("my_op")
struct MyOp:
    @staticmethod
    fn execute[target: StaticString](
        out: OutputTensor,
        inp: InputTensor[dtype=out.dtype, rank=out.rank],
        ctx: DeviceContextPtr,
    ) raises:
        @parameter
        @always_inline
        fn op[width: Int](idx: IndexList[out.rank]) -> SIMD[out.dtype, width]:
            return inp.load[width](idx) * 2

        foreach[op, target=target](out, ctx)
```

**Critical difference:** In stable v25.7, the `foreach` callback **must** have `element_alignment: Int` as a second compile-time parameter. In nightly v26.2+, only `width: Int` is required.

**Don't:**
```mojo
# Wrong imports (won't compile)
from max.tensor import InputTensor, OutputTensor  # Use: from tensor import ...
from max.driver import DeviceContextPtr           # Use: from runtime.asyncrt import ...

# Old API (deprecated)
@compiler.register("my_op", num_dps_outputs=1)
struct MyOp:
    fn execute(out: ManagedTensorSlice, inp: ManagedTensorSlice): ...
```

### Inference Session Configuration

Always specify devices explicitly when creating InferenceSession.

**Pattern:**

```python
from max.engine import InferenceSession
from max.driver import CPU, Accelerator

# CPU inference
session = InferenceSession(devices=[CPU()])

# GPU inference
session = InferenceSession(devices=[Accelerator()])
```

**Don't:**
```python
# No device specified - may default unexpectedly
session = InferenceSession()
```

---

## Common Patterns

### Custom Op Integration Pipeline

**When:** Implementing operations not available in MAX ops, fusing operations for performance, or adding hardware-specific optimizations.

The complete custom op integration pipeline connects Mojo kernels to MAX graphs through `@compiler.register`.

```
Mojo Kernel          @compiler.register        ops.custom()         MAX Graph
   (*.mojo)    --->      decorator      --->   Python call   --->   execution
```

**Step 1 - Mojo Kernel with Registration:**

**Stable (v25.7):**
```mojo
# kernels/my_custom_op.mojo
import compiler
from runtime.asyncrt import DeviceContextPtr
from tensor import InputTensor, OutputTensor, foreach
from utils.index import IndexList

@compiler.register("my_custom_op")
struct MyCustomOp:
    @staticmethod
    fn execute[
        target: StaticString,  # "cpu" or "gpu" - set at compile time
    ](
        output: OutputTensor,
        x: InputTensor[dtype = output.dtype, rank = output.rank],
        ctx: DeviceContextPtr,
    ) raises:
        @parameter
        @always_inline
        # NOTE: v25.7 requires element_alignment parameter
        fn elementwise_op[width: Int, element_alignment: Int](idx: IndexList[output.rank]) -> SIMD[output.dtype, width]:
            return x.load[width](idx) * 2  # Example: double values

        foreach[elementwise_op, target=target](output, ctx)
```

**Step 2 - Python Graph Integration:**

**Stable (v25.7):**
```python
from pathlib import Path
from max.driver import CPU, Accelerator, Buffer, accelerator_count
from max.dtype import DType
from max.engine import InferenceSession
from max.graph import DeviceRef, Graph, TensorType, ops

mojo_kernels = Path(__file__).parent / "kernels"
device = Accelerator() if accelerator_count() > 0 else CPU()

graph = Graph(
    "my_graph",
    forward=lambda x: ops.custom(
        name="my_custom_op",
        device=DeviceRef.from_device(device),
        values=[x],
        out_types=[TensorType(dtype=x.dtype, shape=x.tensor.shape, device=DeviceRef.from_device(device))],
    )[0].tensor,
    input_types=[TensorType(DType.float32, shape=[rows, cols], device=DeviceRef.from_device(device))],
    custom_extensions=[mojo_kernels],
)

session = InferenceSession(devices=[device])
model = session.load(graph)
result = model.execute(Buffer.from_numpy(input_array).to(device))[0]
```

**Nightly (v26.2+):**
```python
import numpy as np
from pathlib import Path
from max.driver import CPU, Accelerator, accelerator_count
from max.dtype import DType
from max.engine import InferenceSession
from max.graph import DeviceRef, Graph, TensorType, ops

mojo_kernels = Path(__file__).parent / "kernels"

# Use DeviceRef.CPU() or DeviceRef.GPU() - NOT DeviceRef.from_device()
device = Accelerator() if accelerator_count() > 0 else CPU()
device_ref = DeviceRef.GPU() if accelerator_count() > 0 else DeviceRef.CPU()

def forward(x):
    # ops.custom signature: name, device, values, out_types
    return ops.custom(
        name="my_custom_op",
        device=device_ref,  # Required positional arg
        values=[x],
        out_types=[TensorType(dtype=x.dtype, shape=x.tensor.shape, device=device_ref)],
    )[0].tensor

# custom_extensions MUST be passed during Graph construction
graph = Graph(
    "my_graph",
    forward=forward,
    input_types=[TensorType(DType.float32, [rows, cols], device=device_ref)],
    custom_extensions=[mojo_kernels],  # Required at construction time
)

session = InferenceSession(devices=[device])
model = session.load(graph)

# Execute with Buffer (v26.2+ uses Buffer, previously Tensor)
from max.driver import Buffer
input_data = np.random.randn(rows, cols).astype(np.float32)
input_buffer = Buffer.from_numpy(input_data).to(device)
result = model.execute(input_buffer)

# Convert output Buffer to numpy
output = result[0].to(CPU()).to_numpy()  # Transfer to CPU first, then to numpy
```

**Common Errors:**
- `DeviceRef has no attribute 'from_device'` → Use `DeviceRef.CPU()` or `DeviceRef.GPU()`
- `custom() missing required argument 'device'` → `device` is now positional before `values`
- `TensorType missing required argument 'device'` → Add `device=device_ref`
- `Could not find mojo kernel` → Ensure `custom_extensions` passed in Graph constructor
- `Failed to resolve module path for MOGGKernelAPI` → Environment issue; reinstall MAX with pixi

**Apple Silicon Notes:**
- Custom ops work on CPU using `DeviceRef.CPU()` and `CPU()` device
- In v26.1+, `accelerator_count()` returns non-zero on Apple Silicon but custom GPU ops may require NVIDIA/AMD
- For development, use CPU device: `device = CPU()` and `device_ref = DeviceRef.CPU()`

**Step 3 - Parameterized Kernels:**
```mojo
# kernels/add_constant.mojo
@compiler.register("add_constant")
struct AddConstant[value: Int]:  # Compile-time parameter
    @staticmethod
    fn execute[target: StaticString](
        output: OutputTensor,
        x: InputTensor[dtype = output.dtype, rank = output.rank],
        ctx: DeviceContextPtr,
    ) raises:
        @parameter
        @always_inline
        fn add_const[width: Int](idx: IndexList[x.rank]) -> SIMD[x.dtype, width]:
            return x.load[width](idx) + Self.value

        foreach[add_const, target=target](output, ctx)
```

```python
# Pass compile-time parameters to kernel
result = ops.custom(
    name="add_constant",
    device=DeviceRef.from_device(device),
    values=[x],
    parameters={"value": 5},  # Maps to struct parameter [value: Int]
    out_types=[TensorType(dtype=x.dtype, shape=x.tensor.shape, device=DeviceRef.from_device(device))],
)[0].tensor
```

Supported parameter types: `bool`, `int`, `str`, `DType`.

---

### Architecture Registration

**When:** Adding new model architectures to MAX pipelines, enabling quantization support for custom models.

**Pattern:**
```python
from max.graph.weights import WeightsFormat
from max.interfaces import PipelineTask
from max.nn.legacy.kv_cache import KVCacheStrategy
from max.pipelines.core import TextContext
from max.pipelines.lib import (
    PIPELINE_REGISTRY,
    RopeType,
    SupportedArchitecture,
    SupportedEncoding,
    TextTokenizer,
)

from .model import MyPipelineModel
from .model_config import MyModelConfig
from . import weight_adapters

my_arch = SupportedArchitecture(
    name="MyModelForCausalLM_Legacy",  # Must match HuggingFace architectures + "_Legacy"
    example_repo_ids=["my-org/my-model-7b", "my-org/my-model-13b"],
    default_encoding=SupportedEncoding.bfloat16,
    supported_encodings={
        SupportedEncoding.bfloat16: [KVCacheStrategy.PAGED],
        SupportedEncoding.q4_k: [KVCacheStrategy.PAGED],
        SupportedEncoding.float8_e4m3fn: [KVCacheStrategy.PAGED],
    },
    pipeline_model=MyPipelineModel,
    tokenizer=TextTokenizer,
    context_type=TextContext,
    default_weights_format=WeightsFormat.safetensors,
    rope_type=RopeType.normal,
    multi_gpu_supported=True,
    weight_adapters={
        WeightsFormat.safetensors: weight_adapters.convert_safetensor_state_dict,
        WeightsFormat.gguf: weight_adapters.convert_gguf_state_dict,
    },
    task=PipelineTask.TEXT_GENERATION,
    config=MyModelConfig,
)

PIPELINE_REGISTRY.register(my_arch)
```

**Required Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | HuggingFace architecture name with `_Legacy` suffix |
| `example_repo_ids` | `list[str]` | HuggingFace repos for testing/validation |
| `default_encoding` | `SupportedEncoding` | Default quantization when not specified |
| `supported_encodings` | `dict` | Encoding-to-cache-strategy mapping |
| `pipeline_model` | `type[PipelineModel]` | Model class with `load_model()` and `execute()` |
| `task` | `PipelineTask` | Task type (TEXT_GENERATION, EMBEDDINGS_GENERATION, etc.) |

**Encoding/Strategy Compatibility:**
- GPU only: `bfloat16`, `float8_e4m3fn`, `float4_e2m1fnx2`, `gptq`
- CPU only: `q4_k`, `q4_0`, `q6_k` (GGUF quantization)
- Universal: `float32`

---

### Offline Batch Inference

**When:** Processing large datasets, running data pipelines, generating training data, or batch evaluation.

**Pattern:**
```python
from max.entrypoints.llm import LLM
from max.pipelines import PipelineConfig

def batch_process(prompts: list[str]) -> list[str]:
    pipeline_config = PipelineConfig(model_path="modularai/Llama-3.1-8B-Instruct-GGUF")
    llm = LLM(pipeline_config)

    # Batch all prompts in a single call - internally parallelized
    return list(llm.generate(prompts, max_new_tokens=50))
```

**Don't:**
```python
# Anti-pattern: HTTP overhead for batch processing
import requests

def batch_process(prompts: list[str]) -> list[str]:
    results = []
    for prompt in prompts:
        response = requests.post(
            "http://localhost:8000/v1/completions",
            json={"prompt": prompt, "max_tokens": 50}
        )
        results.append(response.json()["choices"][0]["text"])
    return results
```

**Memory Optimization for Large Batches:**
```python
from max.pipelines import PipelineConfig
from max.pipelines.kv_cache import KVCacheStrategy

pipeline_config = PipelineConfig(
    model_path="modularai/Llama-3.1-8B-Instruct-GGUF",
    max_batch_size=32,
    max_length=4096,
    cache_strategy=KVCacheStrategy.PAGED,
    device_memory_utilization=0.85,
    enable_chunked_prefill=True,
    max_batch_input_tokens=8192,
)

llm = LLM(pipeline_config)
```

---

### Graph Caching

**When:** Development workflows, CI/CD pipelines, production deployments.

MAX caches compiled kernels for up to 28% faster compilation on subsequent runs.

**Pattern:**
```python
from max.engine import InferenceSession

# First run: full compilation
session = InferenceSession(devices=[Accelerator()])
model = session.load(graph)

# Subsequent runs: cached kernels loaded automatically
# No code changes needed - caching is automatic
```

**Benefits:**
- 28% faster compilation for iterative development
- Shared cache between similar model architectures
- Automatic invalidation when custom ops change

**Note:** Cache is architecture-specific and not portable across targets.

---

### Subgraphs for Device-Aware Scheduling

**When:** Multi-device execution, hybrid CPU/GPU pipelines, conditional computation paths.

**Pattern:**
```python
from max.graph import Graph, TensorType, ops

# Create main graph
main_graph = Graph(TensorType(DType.float32, "batch", 128))

# Add subgraph with device specification
subgraph = main_graph.add_subgraph(
    inputs=[TensorType(DType.float32, "batch", 128)],
    devices=[Accelerator(0)]  # Run on GPU 0
)

# Build subgraph operations
x = subgraph[0]
result = ops.relu(x)
subgraph.output(result)

# Call subgraph from main graph
output = ops.call(subgraph, main_graph[0])
main_graph.output(output)
```

**Note:** Added in v25.7 with `devices` argument.

---

### Complete Custom Model Project Structure

**When:** Building a complete custom model architecture with Mojo layers and MAX serving.

This example shows the recommended project structure for a mixed Mojo/Python model project:

```
my-custom-model/
├── pixi.toml                    # Mojo/MAX dependencies
├── pyproject.toml               # Python dependencies
├── README.md
│
├── model/                       # Pure Mojo model code
│   ├── __init__.mojo
│   ├── config.mojo              # @value struct for model config
│   ├── state.mojo               # Model state with UnsafePointer
│   ├── model.mojo               # Full model assembly
│   └── layers/
│       ├── __init__.mojo
│       ├── attention.mojo       # Attention layer
│       ├── feedforward.mojo     # FFN layer
│       ├── layer_norm.mojo      # Normalization
│       └── embedding.mojo       # Token embeddings
│
├── kernels/                     # Custom GPU ops
│   ├── __init__.mojo
│   └── fused_attention.mojo     # @compiler.register kernels
│
├── serving/                     # Python MAX integration
│   ├── __init__.py
│   ├── architecture.py          # PIPELINE_REGISTRY registration
│   ├── pipeline_model.py        # PipelineModel implementation
│   ├── graph_builder.py         # MAX Graph with custom ops
│   └── tokenizer.py             # Tokenizer wrapper
│
├── weights/                     # Weight conversion
│   └── convert_hf.py            # HuggingFace → MAX format
│
└── tests/
    ├── test_layers.mojo         # Mojo layer tests
    └── test_serving.py          # Python serving tests
```

**pixi.toml (Mojo dependencies):**
```toml
[project]
name = "my-custom-model"
version = "0.1.0"
channels = ["conda-forge", "https://conda.modular.com/max"]
platforms = ["osx-arm64", "linux-64"]

[dependencies]
max = ">=25.1.0"

[tasks]
test = "mojo test tests/"
```

**pyproject.toml (Python dependencies):**
```toml
[project]
name = "my-custom-model"
version = "0.1.0"
dependencies = [
    "torch>=2.0",
    "transformers>=4.30",
    "safetensors",
]

[project.optional-dependencies]
dev = ["pytest"]
```

**Key Integration Points:**

1. **Model layers (Mojo)**: Use `@value` for config, `UnsafePointer` for weights, `Movable` trait for resource ownership
2. **Custom kernels (Mojo)**: Use `@compiler.register` with `InputTensor`/`OutputTensor`
3. **Graph builder (Python)**: Pass kernel directory via `custom_extensions=[Path("kernels")]`
4. **Architecture registration (Python)**: Register with `PIPELINE_REGISTRY` for MAX Serve

**Cross-Reference:** See `mojo-best-practices` patterns:
- `struct-design.md` for model config structs
- `memory-ownership.md` for weight management with UnsafePointer
- `gpu-fundamentals.md` for custom GPU kernels

---

## Decision Guide

| Scenario | Approach | See Also |
|----------|----------|----------|
| Custom GPU kernel | Use `@compiler.register` with `InputTensor`/`OutputTensor` | `mojo:gpu-fundamentals` |
| New model architecture | Register with `PIPELINE_REGISTRY` | `graph-construction.md` |
| Batch data processing | Use `LLM` class for offline inference | `perf-inference.md` |
| Multi-device execution | Use subgraphs with device specification | `multigpu-scaling.md` |
| Faster development iteration | Leverage automatic graph caching | - |

---

## Quick Reference

- **Version alignment**: MAX Python and Mojo versions must match (check with `pip show max` and `mojo --version`)
- **Custom ops**: Use `InputTensor`/`OutputTensor`, not `ManagedTensorSlice`
- **Kernel imports**: `from tensor import InputTensor, OutputTensor, foreach` (not `from max.tensor`)
- **foreach callback (v25.7)**: Must include `element_alignment: Int` parameter: `fn[width: Int, element_alignment: Int](idx)`
- **foreach callback (v26.2+)**: Simpler signature: `fn[width: Int](idx)`
- **DeviceRef (v25.7)**: Use `DeviceRef.from_device(device)`
- **DeviceRef (v26.2+)**: Use `DeviceRef.CPU()` or `DeviceRef.GPU()`
- **ops.custom (v26.2+)**: Signature is `ops.custom(name, device, values, out_types)`
- **custom_extensions**: Must pass during Graph construction, not after
- **InferenceSession**: Always specify `devices=[CPU()]` or `devices=[Accelerator()]`
- **Architecture names**: Must match HuggingFace `architectures` field + `_Legacy` suffix
- **Offline inference**: `LLM` class avoids HTTP overhead for batch jobs
- **Parameter types**: Custom ops support `bool`, `int`, `str`, `DType` parameters
- **Graph caching**: Automatic, provides ~28% faster compilation

---

## Version-Specific Features

### v25.7 (Stable): Custom Ops API

**DeviceRef:** Use `DeviceRef.from_device()`
```python
from max.driver import CPU, Accelerator, accelerator_count
from max.graph import DeviceRef

device = Accelerator() if accelerator_count() > 0 else CPU()
device_ref = DeviceRef.from_device(device)
```

**ops.custom:** Pass device in `out_types`
```python
ops.custom(
    name="my_kernel",
    values=[x],
    out_types=[TensorType(dtype=x.dtype, shape=x.tensor.shape, device=device_ref)],
)[0].tensor
```

**TensorType:** Device parameter is optional
```python
TensorType(DType.float32, shape=[batch, seq], device=device_ref)
```

**Buffer to numpy:** Use `np.array()`
```python
output = np.array(result.to(CPU()))
```

### v26.2+ (Nightly): Custom Ops API

**DeviceRef:** Use static methods
```python
from max.graph import DeviceRef

device_ref = DeviceRef.CPU()    # For CPU
device_ref = DeviceRef.GPU()    # For GPU
device_ref = DeviceRef.GPU(1)   # Specific GPU
```

**ops.custom:** Device is required positional argument
```python
ops.custom(
    name="my_kernel",
    device=device_ref,  # REQUIRED - before values
    values=[x],
    out_types=[TensorType(dtype=x.dtype, shape=x.tensor.shape, device=device_ref)],
)[0].tensor
```

**TensorType:** Device parameter is required
```python
TensorType(DType.float32, [batch, seq], device=device_ref)  # device required
```

**Buffer to numpy:** Use `.to_numpy()`
```python
output = result[0].to(CPU()).to_numpy()  # Transfer to CPU, then to_numpy()
```

**Kernel imports:** Use `from tensor import ...`
```mojo
# Correct (nightly)
from tensor import InputTensor, OutputTensor, foreach
from runtime.asyncrt import DeviceContextPtr

# Wrong - old imports
from max.tensor import ...  # Doesn't exist
```

### Version Comparison

| Task | Stable (v25.7) | Nightly (v26.2+) |
|------|----------------|------------------|
| Create DeviceRef | `DeviceRef.from_device(device)` | `DeviceRef.CPU()` / `DeviceRef.GPU()` |
| Call custom op | `ops.custom(name, values, out_types)` | `ops.custom(name, device, values, out_types)` |
| TensorType device | Optional | Required |
| Buffer to numpy | `np.array(buf.to(CPU()))` | `buf.to(CPU()).to_numpy()` |
| Kernel imports | `from tensor import ...` | `from tensor import ...` |
| **foreach callback** | `fn[width: Int, element_alignment: Int](idx)` | `fn[width: Int](idx)` |

---

## Related Patterns

- [`graph-construction.md`](graph-construction.md) - Building MAX graphs
- [`multigpu-scaling.md`](multigpu-scaling.md) - Multi-GPU deployment
- [`perf-inference.md`](perf-inference.md) - Performance optimization

---

## References

- [MAX Graph API](https://docs.modular.com/max/graph)
- [MAX Pipeline Development](https://docs.modular.com/max/api/python/pipelines/)
- [Offline Inference Documentation](https://docs.modular.com/max/serve/offline-inference)
