# MAX Breaking Changes Reference

> Updated for MAX v25.7+

## v26.2 (Nightly)

| Change | Description |
|--------|-------------|
| KVCache scheduler | Requires replica index for KV cache operations |
| Large runtime layouts | Uses int64 indices for large tensor layouts |
| SM100 kernels | Unified pipeline storage and naming for Blackwell |
| `DeviceRef.from_device()` | **Removed** - use `DeviceRef.CPU()` or `DeviceRef.GPU()` |
| `ops.custom()` signature | `device` is now required positional arg: `ops.custom(name, device, values, out_types)` |
| `TensorType` | Now requires `device` parameter: `TensorType(dtype, shape, device=DeviceRef.CPU())` |
| Custom op kernel imports | Use `from tensor import InputTensor, OutputTensor, foreach` (not `from max.tensor`) |
| Graph `custom_extensions` | Must be passed during Graph construction (not after) |
| `foreach` callback signature | Changed from `fn[width: Int, element_alignment: Int](idx)` to `fn[width: Int](idx)` |

**Critical: Version Alignment**

MAX Python package and Mojo must be version-aligned. Mismatched versions cause kernel compilation failures.

### Quick Version Check

```bash
# Manual check - versions must align
mojo --version          # e.g., Mojo 0.25.7.0 → need MAX 25.7
pip show max | grep Version  # e.g., 25.7.0

# Automated check script (recommended)
./scripts/check-version-alignment.sh
# or
python scripts/check_version_alignment.py
```

### Version Alignment Rules

| Mojo Version | Required MAX Version |
|--------------|---------------------|
| `0.25.7` | `25.7.x` |
| `0.26.1` | `26.1.x` |
| `0.26.2` | `26.2.x` |

### Common Mismatch Errors

**Error: `no matching function in call to 'foreach'`**
```
note: callee parameter 'func' has 'fn[width: Int, element_alignment: Int](IndexList[rank])' type,
      but value has type 'fn[width: Int](idx: IndexList[rank])'
```
- **Cause:** Using nightly callback signature (`fn[width: Int]`) with stable MAX (requires `fn[width: Int, element_alignment: Int]`)
- **Fix:** Check version alignment, use correct signature for your version

**Error: `DeviceRef has no attribute 'from_device'`**
- **Cause:** Using stable API with nightly MAX
- **Fix:** Use `DeviceRef.CPU()` or `DeviceRef.GPU()` on nightly

**Error: `Buffer not found in max.driver`**
- **Cause:** Using nightly API (`Buffer`) with stable MAX
- **Fix:** Use `max.driver.Tensor` on stable v25.7

### How to Fix Mismatches

**Option 1: Use pixi (recommended)**
```bash
# pixi manages both Mojo and MAX versions together
pixi shell  # Always work inside the shell
pixi list | grep -E "^(max|mojo)"  # Verify aligned versions
```

**Option 2: Align pip install with Mojo**
```bash
# For stable Mojo 0.25.7:
pip install max==25.7.0

# For nightly:
pip install --upgrade max --index-url https://whl.modular.com/nightly/simple/
```

**Option 3: Remove conflicting global installs**
```bash
pip uninstall max  # Remove global install
# Then use pixi exclusively
```

## v26.1

| Change | Description |
|--------|-------------|
| `--max-batch-size` semantics | Now per-replica with data parallelism (was aggregate) |
| `--max-ce-batch-size` | Deprecated, use `--max-batch-size` |
| `max.driver.Tensor` | Renamed to `max.driver.Buffer` |
| `prefill_chunk_size` | Renamed to `max_batch_input_tokens` |
| `max_batch_context_length` | Renamed to `max_batch_total_tokens` |
| `--kvcache-ce-watermark` | New option for KVCache scheduling (default 0.95) |
| Llama 3.2 Vision | **Removed** - use Pixtral, InternVL, or Qwen2.5-VL |
| Gemma3 Vision | Added support for 12B and 27B multimodal variants |
| `accelerator_count()` | Now returns non-zero on Apple silicon |
| Stream API | All streams non-blocking (`blocking` arg removed) |
| V1 layer classes | **Removed** (`Conv2dV1`, `LinearV1`, etc.) |
| Python wheels | URL changed to `https://whl.modular.com/nightly/simple/` |
| `max.engine.MojoValue` | Removed |
| `custom_ops_path` | Removed from `InferenceSession.__init__` |

## v25.7 (Stable)

| Change | Description |
|--------|-------------|
| `--do-penalties` | Renamed to `--enable-penalties` (now default) |
| Removed `Conv2dV1`, `LinearV1`, etc. | Use `Conv2d`, `Linear` instead |
| `max.engine.MojoValue` | Removed |
| `custom_ops_path` in InferenceSession | Removed |
| `foreach` callback signature | Requires `element_alignment: Int`: `fn[width: Int, element_alignment: Int](idx)` |
| `max.driver.Buffer` | Use `max.driver.Tensor` (Buffer renamed to Tensor) |
| `KVCacheStrategy` import | Import from `max.kv_cache.registry` or `max.nn.legacy.kv_cache` |

## v25.6

| Change | Description |
|--------|-------------|
| `KVCacheStrategy.CONTINUOUS` | Deprecated, use `PAGED` |
| `ContinuousBatchingKVCacheManager` | Removed |
| `InputContext` | Replaced by `TextGenerationContext`, `EmbeddingsContext` |
| `llguidance` | Replaced `XGrammar` for structured output |

## v25.5

| Change | Description |
|--------|-------------|
| `torch` dependency | Removed from MAX package |
| `PipelineEngine.HUGGINGFACE` | Removed (HuggingFace fallback) |

## v25.4

| Change | Description |
|--------|-------------|
| `max.nn` deprecated layers | Marked as `V1`, new layers are default |
| `ops.select` | Renamed to `ops.where` |
| `MojoCallContextPtr` | Replaced by `DeviceContextPtr` |
| Custom ops | Now use `InputTensor`/`OutputTensor` (not `ManagedTensorSlice`) |

## v25.3

| Change | Description |
|--------|-------------|
| `max-pipelines` CLI | Renamed to `max` |
| `--use-gpu` | Deprecated, use `--devices gpu:0` |
| `--devices=gpu-N` | Changed to `--devices gpu:0,1,2,3` |

## v25.2

| Change | Description |
|--------|-------------|
| `--huggingface-repo-id` | Removed, use `--model-path` |
| `Model.execute()` | Signature changed for GPU support |
| TorchScript models | Removed support |

## CLI Flag Renames Summary

| Old Flag | New Flag | Version |
|----------|----------|---------|
| `--use-gpu` | `--devices gpu:0` | v25.3 |
| `--max-ce-batch-size` | `--max-batch-size` | v26.1 |
| `--do-penalties` | `--enable-penalties` | v25.7 |
| `--prefill-chunk-size` | `--max-batch-input-tokens` | v26.1 |
| `--max-batch-context-length` | `--max-batch-total-tokens` | v26.1 |
| `--ignore-eos` | Use HTTP request payload | v25.6 |

## API Renames Summary

| Old API | New API | Version |
|---------|---------|---------|
| `DeviceRef.from_device(device)` | `DeviceRef.CPU()` / `DeviceRef.GPU()` | v26.2 |
| `ops.custom(name, values, ...)` | `ops.custom(name, device, values, ...)` | v26.2 |
| `from max.tensor import InputTensor` | `from tensor import InputTensor` | v26.2 |
| `TensorType(dtype, shape)` | `TensorType(dtype, shape, device=...)` | v26.2 |
| `max.driver.Tensor` | `max.driver.Buffer` | v26.1 |
| `prefill_chunk_size` | `max_batch_input_tokens` | v26.1 |
| `max_batch_context_length` | `max_batch_total_tokens` | v26.1 |
| `InputContext` | `TextGenerationContext` | v25.6 |
| `ops.select` | `ops.where` | v25.4 |

## Vision Model Support

| Model | Stable (v25.7) | Nightly (v26.2) |
|-------|----------------|-----------------|
| Llama 3.2 Vision | Supported | **Removed** |
| Gemma3 Vision (12B, 27B) | Not available | Supported |
| Pixtral | Supported | Supported |
| InternVL | Supported | Supported |
| Qwen2.5-VL | Supported | Supported |
