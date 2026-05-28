---
name: clean
description: Clean build artifacts and temporary files
user-invocable: true
disable-model-invocation: true
allowed-tools: Bash, Glob
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

5. **General**:
   - `.DS_Store` files
   - `*.log` files
   - `tmp/`, `temp/` directories

## Safety

- Always confirm before deleting `node_modules/`
- Show what will be deleted before executing
- Never delete `.git/` or source files
