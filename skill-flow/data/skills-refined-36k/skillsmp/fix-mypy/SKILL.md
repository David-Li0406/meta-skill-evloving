---
name: fix_mypy
description: 静的解析エラー（MyPy）を効率的に解決するパターン集
---

# Fix MyPy Skills

This skill consolidates specialized knowledge for resolving static analysis errors (MyPy) within the codebase.

## Typical Errors and Solutions

### 1. Errors in Third-party Library Internal Types (e.g., NumPy)

**Symptoms**: `Name "_NBit1" is not defined` or unknown internal types appearing in type hints.
**Solution**: Replace abstract type hints (e.g., `np.complexfloating`, `np.number`) with concrete types (e.g., `np.complex128`, `np.floating`, or a Union thereof). This prevents MyPy from descending into internal representations.

### 2. Method Conflicts due to Multiple Inheritance

**Symptoms**: `Definition of 'mean' in base class ... is incompatible with ...`
**Solution**: Apply `# type: ignore` to the target class definition or add `# type: ignore[misc]` to the conflicting mixin line.

### 3. Array Assignment to Dynamically Generated Lists

**Symptoms**: Errors in assignments like `vals[i][j]` when initialized with `None`.
**Solution**: Annotate explicitly with a concrete type during initialization (e.g., `list[list[Any]]`) or use `cast`.

### 4. Self Type in Mixins

**Symptoms**: Type mismatch when passing `self` within a mixin to a function expecting a concrete class.
**Solution**: Use `cast` to inform MyPy of the runtime type (e.g., `cast("TargetClass", self)`).

### 5. Type Narrowing of External Objects (e.g., Quantity)

**Symptoms**: Errors accessing attributes even when using flags.
**Solution**: Use `isinstance` directly within `if` statements for reliable type narrowing.

### 6. Utilization of Type Aliases

**Solution**: Define complex Union types as `TypeAlias` and reuse them throughout the repository. This enables safe and reliable bulk replacement of concrete types.

### 7. Python 3.9+ Compatibility (PEP 585)

**Symptoms**: `TypeError: 'type' object is not subscriptable` when using `list[...]`, `dict[...]` at runtime, especially if `from __future__ import annotations` is missing or in specific library interactions (e.g. older `astropy`).
**Solution**:

- Ensure `from __future__ import annotations` is present at the top of the file.
- If strictly needed for runtime compatibility without future import, fallback to `typing.List`, `typing.Dict`, etc.
- For `astropy.units.Quantity`, ensure correct usage of generics or string forward references if causing issues.
