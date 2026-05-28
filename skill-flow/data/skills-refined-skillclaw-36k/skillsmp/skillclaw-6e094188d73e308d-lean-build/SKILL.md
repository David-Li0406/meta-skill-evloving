---
name: lean-build
description: Use this skill when building, testing, and debugging Lean 4 projects using Lake, particularly for the ComputationalPaths project.
---

# Lean 4 Build & Debug

This skill covers building, testing, and debugging the ComputationalPaths Lean 4 project using Lake (Lean's build system).

## Project Configuration

**Toolchain**: `leanprover/lean4:v4.24.0` (see `lean-toolchain`)

**Build file**: `lakefile.toml`
```toml
name = "computational_paths"
version = "0.1.0"
defaultTargets = ["computational_paths"]

[[lean_lib]]
name = "ComputationalPaths"

[[lean_exe]]
name = "computational_paths"
root = "Main"
```

## Essential Commands

### Building

```bash
# Build entire project (default targets)
lake build

# Build specific library
lake build ComputationalPaths

# Build specific module
lake build ComputationalPaths.Path.HIT.Circle

# Build executable
lake build computational_paths

# Build with verbose output
lake build -v
```

### Running

```bash
# Run the executable
lake exe computational_paths
```

### Cleaning

```bash
# Clean build artifacts
lake clean

# Full clean (removes .lake directory)
rm -rf .lake && lake build
```

### Updating Dependencies

```bash
# Update lake-manifest.json
lake update

# Resolve and fetch dependencies
lake exe cache get  # if using Mathlib cache
```

## Common Build Errors & Solutions

| Error | Solution |
|-------|----------|
| `type mismatch` | Check that terms have the expected types. Use `@` for explicit arguments or add type annotations. |
| `unknown identifier 'foo'` | Check imports at the top of the file, verify the definition exists in the imported module, and use fully qualified name: `ComputationalPaths.Path.foo`. |
| `failed to synthesize instance` | RwEq is not decidable. Use axioms or `noncomputable` where needed. |
| `universe level mismatch` | Ensure consistent universe variables. HITs typically use `Type u`. |
| `must be marked as 'noncomputable'` | Add `noncomputable` keyword: `noncomputable def foo := ...`. |

## Debugging

```lean
#check myTerm             -- show type
#print axioms myTheorem   -- show axioms used
#reduce myTerm            -- fully normalize
```