---
name: ci-and-releases
description: Use this skill when you need a checklist for maintaining CI, performing toolchain and version bumps, and ensuring release hygiene in a Lean 4 project.
---

# CI & Releases

This skill provides a repeatable checklist for keeping the repository green on CI and preparing small “release-like” changes (toolchain bump, version bump, dependency updates).

## CI Mental Model

CI is essentially “clean checkout + `lake build`”. Keep changes compatible with:
- The current toolchain in `lean-toolchain`
- Dependencies pinned by `lake-manifest.json`
- The project’s “zero-warning” expectations (treat warnings as failures to fix immediately)

## Local Verification

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
2. Run the build command to confirm:
   - For Unix: `lake build`
   - For Windows: `.\lake.cmd build`
3. Run the executable to confirm the output:
   - For Unix: `lake exe computational_paths`
   - For Windows: `.\lake.cmd exe computational_paths`
4. If the bump is user-visible, update `README.md` or add a short changelog note.

## Toolchain Bump Checklist

When updating `lean-toolchain`:
1. Edit `lean-toolchain`
2. Run the build command:
   - For Unix: `lake build`
   - For Windows: `.\lake.cmd build`
3. If dependencies need repinning, run `lake update` and rebuild.
4. Ensure CI config still matches expectations (`.github/workflows/*`).

## Dependency Update Checklist

If updating dependencies (manifest changes):
1. Run `lake update`.
2. Build the project:
   - For Unix: `lake build`
   - For Windows: `.\lake.cmd build`
3. Fix any breakage by updating imports/lemmas or pinning versions back as needed.