---
name: clean-build-artifacts
description: Use this skill to clean build artifacts and reset the project state across various programming environments.
---

# Clean Build Artifacts

Remove build artifacts and temporary files from your project.

## What to Clean

1. **Python**:
   - `__pycache__/` directories
   - `*.pyc`, `*.pyo` files
   - `.pytest_cache/`
   - `.ruff_cache/`
   - `dist/`, `build/`, `*.egg-info/`

2. **Rust**:
   - `target/` directory (`cargo clean`)

3. **Go**:
   - `bin/` directory (if exists)
   - `go clean -cache` (optional, ask first)

4. **Node.js**:
   - `node_modules/` (ask first - takes time to reinstall)
   - `dist/`, `build/`
   - `.next/`, `.nuxt/` (framework caches)

5. **Xcode**:
   - Clean build using:
     ```bash
     xcodebuild -scheme <YourScheme> clean 2>&1 | tail -5
     ```
   - Remove DerivedData (optional, for deep clean):
     ```bash
     rm -rf ~/Library/Developer/Xcode/DerivedData/<YourScheme>-*
     echo "DerivedData cleaned"
     ```
   - Reset Simulator (optional):
     ```bash
     xcrun simctl terminate booted <YourAppIdentifier> 2>/dev/null || true
     xcrun simctl uninstall booted <YourAppIdentifier> 2>/dev/null || true
     echo "Simulator reset"
     ```

6. **General**:
   - `.DS_Store` files
   - `*.log` files
   - `tmp/`, `temp/` directories

## Safety

- Always confirm before deleting `node_modules/`
- Show what will be deleted before executing
- Never delete `.git/` or source files

## Verification

- For Xcode, check no cached builds:
  ```bash
  ls ~/Library/Developer/Xcode/DerivedData/ | grep -c <YourScheme> || echo "Clean"
  ```

## Output

```
Build artifacts cleaned.
Ready for fresh build.
```