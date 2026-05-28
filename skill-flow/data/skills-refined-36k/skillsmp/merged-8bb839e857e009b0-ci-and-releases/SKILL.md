---
name: ci-and-releases
description: Use this skill for maintaining CI hygiene, managing toolchain and version bumps, and preparing release-like changes in the ComputationalPaths Lean 4 project.
---

# CI & Releases

This skill provides a repeatable checklist for keeping the repository green on CI and preparing small “release-like” changes, including toolchain bumps, version bumps, and dependency updates.

## CI Mental Model

CI is essentially a “clean checkout + `lake build`”. Ensure changes are compatible with:
- The current toolchain specified in `lean-toolchain`
- Dependencies pinned in `lake-manifest.json`
- The project’s “zero-warning” expectations (treat warnings as failures to fix immediately)

## Local CI Verification

From the Lean project root (`computational_paths/`):

### For Unix-based Systems

```bash
# Build
lake build

# Run executable
lake exe computational_paths

# Clean rebuild if needed
lake clean && lake build
```

### For Windows

```powershell
# Build
.\lake.cmd build

# Run executable
.\lake.cmd exe computational_paths

# Clean rebuild if needed
.\lake.cmd clean
.\lake.cmd build
```

## Version Bump Checklist

This repository exposes a version string:
- `ComputationalPaths/Basic.lean` defines `libraryVersion`
- `Main.lean` prints it via the executable

When bumping the version:
1. Update `ComputationalPaths/Basic.lean` (`libraryVersion`)
2. Build and run the executable to confirm the output
3. If the bump is user-visible, update `README.md` or add a short changelog note

## Toolchain Bump Checklist

When updating `lean-toolchain`:
1. Edit `lean-toolchain`
2. Build the project
3. If dependencies need repinning, run `lake update` and rebuild
4. Ensure CI configuration still matches expectations (`.github/workflows/*`)

## Dependency Update Checklist

If updating dependencies (manifest changes):
1. Run `lake update`
2. Build the project
3. Fix any breakage by updating imports/lemmas or pinning versions back as needed

## CI Configuration

GitHub Actions uses `leanprover/lean-action@v1`:

```yaml
# .github/workflows/lean_action_ci.yml
name: Lean Action CI
on: [push, pull_request, workflow_dispatch]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: leanprover/lean-action@v1
```