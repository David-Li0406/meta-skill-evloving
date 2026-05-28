---
name: lean-build
description: Build, test, and debug Lean 4 projects using Lake. Use when building the ComputationalPaths project, checking for errors, running tests, cleaning artifacts, or debugging Lean 4 compilation issues.
---

# Lean 4 Build & Debug

Build the ComputationalPaths Lean 4 project using Lake.

## Essential Commands

```bash
# Build entire project
lake build

# Build specific module
lake build ComputationalPaths.Path.HIT.Circle

# Clean and rebuild
lake clean && lake build

# Run executable
lake exe computational_paths
```

## Common Build Errors

| Error | Solution |
|-------|----------|
| `unknown identifier` | Check imports, use fully qualified name |
| `type mismatch` | Add type annotations or use `@` for explicit args |
| `must be marked as 'noncomputable'` | Add `noncomputable` keyword |
| `universe level mismatch` | Ensure consistent universe variables (typically `Type u`) |

## Debugging

```lean
#check myTerm             -- show type
#print axioms myTheorem   -- show axioms used
#reduce myTerm            -- fully normalize
```

## Toolchain

- Current: `leanprover/lean4:v4.24.0` (see `lean-toolchain`)
- Update: edit `lean-toolchain`, then `lake clean && lake build`
