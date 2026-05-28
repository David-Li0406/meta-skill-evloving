---
name: extend_gwpy
description: GWpy/Astropyクラスの安全な継承と拡張のためのガイドライン
---

# Extend GWpy Class

This skill provides guidelines and patterns for safely inheriting from and extending GWpy/Astropy classes (TimeSeries, FrequencySeries, Spectrogram, etc.).

## Common Pitfalls & Solutions

### 1. `__new__` and Metadata

GWpy uses `__new__` to preserve units and metadata. When subclassing, ensure metadata is propagated.

```python
class MyTimeSeries(TimeSeries):
    def __new__(cls, data, *args, **kwargs):
        obj = super().__new__(cls, data, *args, **kwargs)
        return obj
```

### 2. Unit Preservation

Always ensure that mathematical operations preserve units.

### 4. Metadata Preservation in `__array_finalize__`

When using NumPy ufuncs (like `+`, `*`) or arithmetic operations, NumPy creates new instances and calls `__array_finalize__(self, obj)`. `obj` is the original instance. You must copy your custom metadata from `obj` to preserve it.

```python
def __array_finalize__(self, obj):
    super().__array_finalize__(obj)
    if obj is None:
        return
    
    # Preserve custom attributes
    for attr in ["_my_meta", "_domain_label"]:
        val = getattr(obj, attr, None)
        if val is not None:
            setattr(self, attr, val)
```

**CRITICAL PITFALL**: If `__new__` sets default values (e.g., `self.attr = "default"`), then `__array_finalize__` might see those defaults and decide not to copy from `obj`.
*   **Solution**: Initialize custom attributes to `None` in `__new__` and handle default logic within `__array_finalize__`.
*   **Reference**: See `gwexpy/types/array4d.py` for how it handles `_axis0_index`. It defers setting the `arange` default until after it fails to find an index on `obj`.

**Note**: Be careful if the metadata depends on the axis names or shape, which might have changed (though ufuncs usually preserve these). Use the pattern in `Array4D` and `FieldBase` as a reference.

### 5. Type Preservation in Collections

When implementing batch methods in collection classes (like `FieldList` or `FieldDict`), use `self.__class__` to ensure that subclasses return instances of their own type.

```python
def map_all(self, func):
    return self.__class__([func(item) for item in self])
```
