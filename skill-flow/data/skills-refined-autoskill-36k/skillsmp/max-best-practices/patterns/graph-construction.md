---
title: MAX Graph Construction
description: Graph building patterns including lazy context, modules, symbolic dimensions, and pipeline models
impact: HIGH
category: graph
tags: graph, construction, modules, symbolic-dims, pipeline
error_patterns:
  - "Graph"
  - "TensorType"
  - "symbolic dimension"
  - "shape mismatch"
  - "compilation"
  - "module"
scenarios:
  - "Build MAX Graph from scratch"
  - "Use symbolic dimensions"
  - "Create reusable modules"
  - "Implement pipeline model"
  - "Fix graph compilation errors"
  - "Configure lazy context"
consolidates:
  - graph-construction.md
  - graph-lazy-context.md
  - graph-modules.md
  - graph-symbolic-dims.md
  - graph-pipeline-model.md
---

# MAX Graph Construction

**Category:** graph | **Impact:** HIGH

Comprehensive patterns for MAX Graph construction including proper type specifications, lazy context for efficient compilation, reusable modules, symbolic dimensions for dynamic shapes, and pipeline model implementation.

---

## Core Concepts

### Graph Type Specifications

Specify input types explicitly when constructing graphs.

**Pattern:**

```python
from max.graph import Graph, TensorType, ops
from max.dtype import DType

# Explicit input types with symbolic dimensions
graph = Graph(
    TensorType(DType.float32, "batch", 128),  # [batch, 128]
)

# Access inputs by index
x = graph[0]

# Add operations
result = ops.relu(x @ weight)

# Define outputs
graph.output(result)

# Verify graph is valid
graph.verify()
```

**Don't:**
```python
# No input type specification
graph = Graph()
```

### Symbolic Dimensions

Use `AlgebraicDim` for named dynamic dimensions that must match across tensors.

**Pattern:**

```python
from max.graph import Graph, TensorType, AlgebraicDim

batch = AlgebraicDim("batch")

# Named dims that must match
graph = Graph(
    TensorType(DType.float32, batch, 128),  # [batch, 128]
    TensorType(DType.float32, batch, 256),  # [batch, 256] - same batch!
)

# Algebraic expressions
seq_len = AlgebraicDim("seq")
padded = seq_len + 4  # Compile-time expression
```

**Don't:**
```python
# Anonymous dynamic dims - no matching enforcement
graph = Graph(
    TensorType(DType.float32, None, 128),  # [?, 128]
    TensorType(DType.float32, None, 128),  # [?, 128] - different!
)
```

**Note:** Algebraic expressions simplify canonically: `-x - 4 == -(x + 4)`.

---

## Common Patterns

### Lazy Context for Graph Building

**When:** Building complex neural network graphs, implementing custom model architectures, optimizing memory allocation during model loading.

Use `F.lazy()` context manager to defer tensor creation during model construction.

**Pattern:**
```python
from max import functional as F
from max.nn import Module

class GptOssModel(PipelineModel):
    def load_model(self):
        # Build input types
        tokens_type = TensorType(DType.int64, shape=["total_seq_len"], device=device_ref)

        # Lazy context defers tensor realization
        with F.lazy():
            nn_model = GptOss(model_config, self.kv_manager)
            nn_model.to(self.devices[0])

        # Compile with concrete types
        compiled_model = nn_model.compile(
            tokens_type,
            return_n_logits_type,
            input_row_offsets_type,
            *kv_types,
            weights=state_dict,
        )
        return compiled_model
```

**Don't:**
```python
# Tensors allocated immediately (may not be optimal for compilation)
model = MyModel()
model.to(device)  # Immediate transfer
```

**Correct:**
```python
# Tensors deferred until compilation
with F.lazy():
    model = MyModel()
    model.to(device)  # Recorded, not executed

# Compile triggers optimized allocation
compiled = model.compile(input_types, weights=weights)
```

**How it works:**
1. Within `F.lazy()`, tensor operations are recorded, not executed
2. Model structure is captured as a graph
3. `compile()` triggers optimization and allocation
4. Weights can be loaded externally via `weights=` parameter
5. Parameters automatically become graph weights

---

### Module-Based Architecture

**When:** Custom model architectures, reusable layer libraries, weight management.

Use `max.nn.Module` base class for building reusable neural network layers.

**Pattern:**
```python
from max.nn import Module, Linear, Sequential

class MLP(Module):
    def __init__(self, hidden_dim: int, output_dim: int):
        super().__init__()
        self.fc1 = Linear(hidden_dim)
        self.fc2 = Linear(output_dim)

    def forward(self, x):
        return self.fc2(ops.gelu(self.fc1(x)))

# Use with state_dict for weight loading
mlp = MLP(512, 256)
mlp.load_state_dict(weights)
```

**Don't:**
```python
# Ad-hoc layer construction
def create_mlp(x, w1, w2):
    return ops.gelu(x @ w1) @ w2
```

**Module Compilation Pattern:**
```python
from max.nn import Module, module_dataclass
from max.tensor import Tensor, TensorType

@module_dataclass
class Linear(Module):
    weight: Tensor
    bias: Tensor

    def forward(self, x: Tensor) -> Tensor:
        return x @ self.weight.T + self.bias

# Create module with initial weights
linear = Linear(
    weight=Tensor.zeros([10, 5]),
    bias=Tensor.zeros([10])
)

# Compile with input type specification
input_type = TensorType(DType.float32, [3, 5], device=device)
compiled = linear.compile(input_type)

# Execute compiled model
result = compiled(Tensor.ones([3, 5]))
```

**Note:** `Module` ensures unique weight names and supports `state_dict()`.

---

### PipelineModel Implementation

**When:** Implementing new model architectures for MAX Serve, adding custom models, building production inference pipelines.

Use the `PipelineModel` base class with `KVCacheMixin` for text generation models.

**Pattern:**
```python
from max.pipelines.lib import PipelineModel, KVCacheMixin, PipelineConfig
from max.engine import InferenceSession

class MyModel(PipelineModel[TextContext], KVCacheMixin):
    def __init__(
        self,
        pipeline_config: PipelineConfig,
        session: InferenceSession,
        huggingface_config: AutoConfig,
        encoding: SupportedEncoding,
        devices: list[Device],
        kv_cache_config: KVCacheConfig,
        weights: Weights,
        adapter: WeightsAdapter | None = None,
        return_logits: ReturnLogits = ReturnLogits.LAST_TOKEN,
    ):
        super().__init__(...)
        self.model = self.load_model()

    @staticmethod
    def calculate_max_seq_len(pipeline_config, huggingface_config) -> int:
        """Calculate maximum sequence length."""
        return pipeline_config.max_length or huggingface_config.max_position_embeddings

    @classmethod
    def get_kv_params(cls, huggingface_config, pipeline_config, devices, kv_cache_config, cache_dtype) -> KVCacheParams:
        """Configure KV cache parameters."""
        return MyConfig.construct_kv_params(...)

    def load_model(self) -> Callable[..., Any]:
        """Build and compile the model graph."""
        device_ref = DeviceRef.from_device(self.devices[0])
        tokens_type = TensorType(DType.int64, shape=["total_seq_len"], device=device_ref)

        with F.lazy():
            nn_model = MyNN(model_config, self.kv_manager)
            nn_model.to(self.devices[0])

        compiled_model = nn_model.compile(
            tokens_type,
            return_n_logits_type,
            input_row_offsets_type,
            *kv_types,
            weights=state_dict,
        )
        return compiled_model

    def execute(self, model_inputs: ModelInputs) -> ModelOutputs:
        """Execute model and return outputs."""
        model_outputs = self.model(
            model_inputs.tokens,
            model_inputs.return_n_logits,
            model_inputs.input_row_offsets,
            *model_inputs.kv_cache_inputs,
        )
        return ModelOutputs(logits=model_outputs[0].driver_tensor)
```

**Don't:**
```python
# Not compatible with MAX Serve, no KV cache management
class MyModel:
    def generate(self, prompt):
        return self.model(prompt)
```

**Required Methods:**

| Method | Purpose |
|--------|---------|
| `calculate_max_seq_len()` | Determine max context length |
| `get_kv_params()` | Configure KV cache |
| `load_model()` | Build and compile graph |
| `execute()` | Run inference |
| `prepare_initial_token_inputs()` | Prepare input buffers |

---

### Architecture Registration

**When:** Adding models to MAX Serve, enabling quantization support.

```python
from max.pipelines.lib.registry import SupportedArchitecture, PIPELINE_REGISTRY

my_architecture = SupportedArchitecture(
    name="MyModelForCausalLM",  # Must match HuggingFace architectures
    example_repo_ids=["your-org/your-model"],
    default_encoding=SupportedEncoding.bfloat16,
    supported_encodings={
        SupportedEncoding.bfloat16: [KVCacheStrategy.PAGED],
        SupportedEncoding.q4_k: [KVCacheStrategy.PAGED],
    },
    pipeline_model=MyModel,
    tokenizer=TextTokenizer,
    default_weights_format=WeightsFormat.safetensors,
    rope_type=RopeType.none,
    weight_adapters={
        WeightsFormat.safetensors: convert_safetensor_state_dict,
    },
    multi_gpu_supported=True,
    task=PipelineTask.TEXT_GENERATION,
    context_type=TextContext,
)

PIPELINE_REGISTRY.register(my_architecture)
```

**Pipeline Factory Usage:**
```python
from max.pipelines import PIPELINE_REGISTRY, PipelineConfig, PipelineTask

# Retrieve tokenizer and pipeline factory
tokenizer, pipeline_factory = PIPELINE_REGISTRY.retrieve_factory(
    pipeline_config,
    task=PipelineTask.TEXT_GENERATION,
)

# Create pipeline (lazy construction)
pipeline = pipeline_factory()

# Generate text
response = pipeline.generate(
    prompt="Hello, world!",
    max_tokens=100,
)
```

---

## Decision Guide

| Scenario | Approach | See Also |
|----------|----------|----------|
| Dynamic batch size | Use `AlgebraicDim("batch")` | - |
| Variable sequence length | Use `AlgebraicDim("seq")` | - |
| Complex model architecture | Use `F.lazy()` context | - |
| Reusable layers | Extend `Module` base class | - |
| MAX Serve integration | Implement `PipelineModel` | `engine-operations.md` |
| Weight management | Use `state_dict()` / `load_state_dict()` | - |

---

## Quick Reference

- **Input types**: Always specify explicitly with `TensorType`
- **Symbolic dims**: Use `AlgebraicDim("name")` for dimensions that must match
- **Lazy context**: Use `F.lazy()` for deferred tensor creation
- **Modules**: Extend `Module` for reusable layers with automatic weight management
- **Pipeline models**: Implement `load_model()` and `execute()` methods
- **Verification**: Call `graph.verify()` to validate graph structure

---

## Best Practices

- Always use `F.lazy()` for model construction in pipelines
- Specify input types for proper graph tracing
- Use `@module_dataclass` for type-safe module definitions
- Load weights after compilation for memory efficiency
- Architecture name must match HuggingFace config `architectures` field
- Use ragged tensors for variable-length batching (avoids padding)

---

## Related Patterns

- [`engine-operations.md`](engine-operations.md) - Custom operations and architecture registration
- [`model-loading.md`](model-loading.md) - Supported architectures and weight formats
- [`perf-inference.md`](perf-inference.md) - Performance optimization

---

## References

- [MAX Graph API](https://docs.modular.com/max/graph)
- [MAX Pipeline Development](https://docs.modular.com/max/api/python/pipelines/)
