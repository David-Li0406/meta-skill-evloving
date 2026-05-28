---
name: tauri-sidecar-troubleshoot
description: Troubleshoot Tauri sidecar, Rust build, and dev/production mode issues
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: debugging
---

# Tauri Sidecar Troubleshooting Guide

Use this skill when debugging issues with Tauri sidecars, especially Bun-based sidecars that can operate in both development and production modes.

## Architecture Overview

This project uses a **dual-mode sidecar** pattern:

| Mode            | Sidecar Binary  | Behavior                                      |
| --------------- | --------------- | --------------------------------------------- |
| **Development** | Bun runtime     | Runs `bun run api/server.ts` from source code |
| **Production**  | Compiled binary | Has code baked in, ignores script arguments   |

### Key Files

- `src-tauri/binaries/bun-sidecar-{arch}` - The sidecar binary (e.g., `bun-sidecar-aarch64-apple-darwin`)
- `src-tauri/src/lib.rs` - Rust code that spawns the sidecar
- `Makefile` - Build targets for dev and production

### How Mode Detection Works

In `lib.rs`, development mode is detected by checking if the resource directory contains build output paths:

```rust
let is_dev_mode = resource_dir.to_string_lossy().contains("target/debug")
    || resource_dir.to_string_lossy().contains("target/release");
```

## Common Problems & Solutions

### Problem 1: "Not Found" errors for API routes in dev mode

**Symptoms:**

- `make dev` returns 404 for endpoints that work in `make dev-browser`
- New API routes are not being recognized
- Route count differs between modes (e.g., 91 routes vs 97 routes)

**Root Cause:**
The sidecar binary is a **compiled binary** (from a previous `make build`) instead of the **Bun runtime**. When compiled, the sidecar ignores the `bun run api/server.ts` arguments and runs its embedded (potentially stale) code.

**Solution:**

```bash
# Check if sidecar is Bun runtime or compiled binary
./src-tauri/binaries/bun-sidecar-aarch64-apple-darwin --version
# If it shows a Bun version (e.g., "1.1.38"), it's the runtime
# If it errors or shows app info, it's a compiled binary

# Replace with Bun runtime
make prepare-dev-sidecar

# Or use the auto-detection target
make ensure-dev-sidecar
```

**Prevention:**
The `make dev` target should call `ensure-dev-sidecar` first to auto-detect and fix this.

---

### Problem 2: Stale Cargo incremental compilation cache

**Symptoms:**

- Fixed the sidecar binary, but dev mode still behaves incorrectly
- Route count or behavior doesn't match expectations
- Changes to `lib.rs` don't seem to take effect

**Root Cause:**
Cargo's incremental compilation cache in `src-tauri/target/` contains stale artifacts.

**Solution:**

```bash
# Clean the Cargo cache
cd src-tauri && cargo clean

# Or just touch the lib.rs to force recompilation
touch src-tauri/src/lib.rs
```

---

### Problem 3: Sidecar not starting or port not detected

**Symptoms:**

- App starts but shows connection errors
- "Failed to get backend port" or similar errors
- Sidecar process exits immediately

**Debugging Steps:**

1. **Check sidecar stdout** - Add debug logging to `lib.rs`:

```rust
CommandEvent::Stdout(line_bytes) => {
    let line = String::from_utf8_lossy(&line_bytes);
    println!("[Sidecar] {}", line);  // Print all output
    // ...
}
```

2. **Run sidecar manually**:

```bash
cd src-tauri
DATA_DIR=../data ./binaries/bun-sidecar-aarch64-apple-darwin run ../api/server.ts
```

3. **Check for port conflicts**:

```bash
lsof -i :3000
```

---

### Problem 4: Production build works but dev mode fails (or vice versa)

**Symptoms:**

- `make build` creates a working app but `make dev` fails
- Or `make dev` works but the built DMG doesn't

**Key Differences:**

| Aspect        | Dev Mode               | Production          |
| ------------- | ---------------------- | ------------------- |
| Sidecar       | Bun runtime            | Compiled binary     |
| Code source   | `api/server.ts` (live) | Embedded in binary  |
| Data dir      | Relative `./data`      | From `DATA_DIR` env |
| Resource path | `target/debug/`        | App bundle          |

**Debugging:**

1. Check `is_dev_mode` detection in `lib.rs`
2. Verify the correct sidecar arguments are passed for each mode
3. Check environment variables (`DATA_DIR`, `PORT`)

---

## Makefile Targets Reference

```makefile
# Development
make dev                  # Start Tauri dev mode (auto-ensures Bun sidecar)
make dev-browser          # Start without Tauri (direct bun run)
make ensure-dev-sidecar   # Check/fix sidecar to be Bun runtime
make prepare-dev-sidecar  # Force download Bun runtime for sidecar

# Production
make build               # Build production app (compiles sidecar)
make build-sidecar       # Compile sidecar binary only

# Debugging
make logs                # View sidecar/app logs
make logs-clear          # Clear log files
```

---

## The ensure-dev-sidecar Pattern

The `ensure-dev-sidecar` target automatically detects and fixes the sidecar:

```makefile
ensure-dev-sidecar:
	@SIDECAR="src-tauri/binaries/bun-sidecar-aarch64-apple-darwin"; \
	if [ ! -f "$$SIDECAR" ]; then \
		echo "Sidecar not found, downloading Bun runtime..."; \
		$(MAKE) prepare-dev-sidecar; \
	elif ! "$$SIDECAR" --version 2>/dev/null | grep -qE '^[0-9]+\.[0-9]+'; then \
		echo "Sidecar is compiled binary, replacing with Bun runtime..."; \
		$(MAKE) prepare-dev-sidecar; \
	else \
		echo "✓ Dev sidecar is Bun runtime"; \
	fi
```

**How it works:**

1. Check if sidecar exists
2. Run `--version` on it
3. If output looks like a version number (e.g., `1.1.38`), it's Bun runtime
4. If not, replace it with a fresh Bun runtime download

---

## Quick Diagnosis Checklist

When Tauri/sidecar issues occur, check in order:

1. **Is the sidecar the right type?**

   ```bash
   ./src-tauri/binaries/bun-sidecar-* --version
   ```

2. **Is Cargo cache stale?**

   ```bash
   cd src-tauri && cargo clean && cd ..
   ```

3. **Are there port conflicts?**

   ```bash
   lsof -i :3000
   ```

4. **What's the sidecar outputting?**
   - Check logs: `make logs`
   - Or add `println!("[Sidecar] {}", line);` to lib.rs

5. **Does the API work standalone?**
   ```bash
   cd api && bun run server.ts
   curl http://localhost:3000/api/health
   ```

---

## Key Insight

The fundamental insight is that a **Bun sidecar binary can be either**:

- The **Bun runtime** itself (can run any `.ts` file)
- A **compiled binary** (has specific code baked in, ignores arguments)

Both are valid executables, but they behave completely differently. Always verify which type you have when debugging!
