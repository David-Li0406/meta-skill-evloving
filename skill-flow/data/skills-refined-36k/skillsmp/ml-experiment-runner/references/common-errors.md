# Common ML Experiment Errors and Fixes

## Table of Contents
- [Tensor/Numpy Conversion Errors](#tensornumpy-conversion-errors)
- [JSON Serialization Errors](#json-serialization-errors)
- [Library API Changes](#library-api-changes)
- [Memory Errors](#memory-errors)
- [Shape Mismatches](#shape-mismatches)

## Tensor/Numpy Conversion Errors

### RuntimeError: Can't call numpy() on Tensor that requires grad

**Error:**
```python
RuntimeError: Can't call numpy() on Tensor that requires grad. Use tensor.detach().numpy() instead.
```

**Cause:** Calling `.numpy()` on a tensor that's part of the computation graph.

**Fix:** Add `.detach()` before `.cpu().numpy()`:
```python
# Wrong
values = tensor.cpu().numpy()

# Correct
values = tensor.detach().cpu().numpy()
```

**Prevention:** Search for all `.cpu().numpy()` patterns and add `.detach()`:
```bash
grep -n "\.cpu()\.numpy()" handlers/p2/*.py
```

### RuntimeError: Can't convert CUDA tensor to numpy

**Fix:** Move to CPU first:
```python
values = tensor.detach().cpu().numpy()
```

## JSON Serialization Errors

### TypeError: Object of type bool_ is not JSON serializable

**Cause:** NumPy types (bool_, int64, float32) aren't JSON serializable.

**Fix:** Convert to Python native types:
```python
import numpy as np

def to_python_types(obj):
    """Recursively convert numpy types to Python types."""
    if isinstance(obj, dict):
        return {k: to_python_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_python_types(v) for v in obj]
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

# Use before JSON serialization
clean_data = to_python_types(results_data)
json.dump(clean_data, f)
```

**Quick fixes for specific types:**
```python
# bool_ → bool
bool(np.bool_(True))

# int64 → int
int(np.int64(42))

# float32 → float
float(np.float32(3.14))

# ndarray → list
array.tolist()
```

## Library API Changes

### KeyError with DINOv2 output

**Error:**
```python
KeyError: 'x_norm'
```

**Cause:** DINOv2 output format varies by version.

**Fix:** Use robust key handling:
```python
features = model.forward_features(images)
if isinstance(features, dict):
    if 'x_norm_patchtokens' in features:
        patch_features = features['x_norm_patchtokens']
    elif 'x_prenorm' in features:
        patch_features = features['x_prenorm'][:, 1:, :]
    elif 'x_norm' in features:
        patch_features = features['x_norm'][:, 1:, :]
    else:
        # Fallback: find first 3D tensor
        for key, val in features.items():
            if isinstance(val, torch.Tensor) and len(val.shape) == 3:
                patch_features = val[:, 1:, :] if val.shape[1] > 256 else val
                break
else:
    patch_features = features[:, 1:, :]  # Exclude CLS token
```

### Transformers/Diffusers API changes

**Prevention:** Pin versions in requirements or check return types:
```python
output = model.generate(...)
# Handle both old and new API
if hasattr(output, 'sequences'):
    tokens = output.sequences
else:
    tokens = output
```

## Memory Errors

### CUDA out of memory

**Fixes:**
1. Use bfloat16 instead of float32:
   ```python
   model = model.to(torch.bfloat16)
   ```

2. Clear cache between operations:
   ```python
   torch.cuda.empty_cache()
   ```

3. Use gradient checkpointing for training:
   ```python
   model.gradient_checkpointing_enable()
   ```

4. Reduce batch size:
   ```python
   batch_size = 8  # Instead of 16
   ```

5. Process in chunks:
   ```python
   for i in range(0, len(data), chunk_size):
       chunk = data[i:i+chunk_size]
       with torch.no_grad():
           process(chunk)
       torch.cuda.empty_cache()
   ```

## Shape Mismatches

### RuntimeError: shape mismatch

**Debug steps:**
1. Print shapes at each step:
   ```python
   print(f"Input shape: {x.shape}")
   print(f"After conv: {conv_out.shape}")
   print(f"Expected: {expected_shape}")
   ```

2. Check dimension ordering (NCHW vs NHWC)

3. Verify batch dimension is preserved

**Common fixes:**
```python
# Add batch dimension
x = x.unsqueeze(0)

# Remove batch dimension
x = x.squeeze(0)

# Permute dimensions
x = x.permute(0, 3, 1, 2)  # NHWC → NCHW

# Reshape
x = x.view(batch_size, -1)
```
