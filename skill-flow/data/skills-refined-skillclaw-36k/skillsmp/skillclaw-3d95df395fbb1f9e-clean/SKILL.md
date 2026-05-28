---
name: clean
description: Use this skill to remove build artifacts and temporary files across various programming environments.
---

# Clean Project

Remove build artifacts and temporary files.

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
     xcodebuild -scheme YourScheme clean
     ```
   - Remove DerivedData (optional, for deep clean):
     ```bash
     rm -rf ~/Library/Developer/Xcode/DerivedData/YourProject-*
     ```

6. **General**:
   - `.DS_Store` files
   - `*.log` files
   - `tmp/`, `temp/` directories

## Safety

- Always confirm before deleting `node_modules/`
- Show what will be deleted before executing
- Never delete `.git/` or source files
- For Xcode, ensure to stop the app if running and uninstall it from the simulator if necessary.

## Verification

- Check for any remaining cached builds:
  ```bash
  ls ~/Library/Developer/Xcode/DerivedData/ | grep -c YourProject || echo "Clean"
  ```

## Output

```
Build artifacts cleaned.
Ready for fresh build.
```