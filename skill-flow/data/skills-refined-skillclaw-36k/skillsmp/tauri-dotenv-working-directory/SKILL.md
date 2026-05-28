---
name: tauri-dotenv-working-directory
description: |
  Fix for Tauri app not loading .env file with dotenvy. Use when: (1) Environment
  variables return "not set" errors in Tauri commands, (2) dotenvy::from_filename()
  fails with relative paths like "../../.env", (3) API keys or config work locally
  but not in Tauri app, (4) GhostClient::from_env() or similar fails with missing
  env vars. The fix is that `cargo tauri dev` runs with CWD at project root, not
  at ui/src-tauri, so use ".env" not "../../.env".
author: Claude Code
version: 1.0.0
date: 2025-01-23
---

# Tauri Dotenvy Working Directory Fix

## Problem
When adding `dotenvy` to a Tauri app to load environment variables, relative paths
like `../../.env` fail because the working directory during `cargo tauri dev` is
not what you'd expect from the file structure.

## Context / Trigger Conditions

**Error symptoms:**
- `GHOST_URL not set` or similar "env var not set" errors
- `GhostClient::from_env()` or API clients fail to initialize
- `dotenvy::from_filename("../../.env")` returns Err
- App works when env vars are exported manually but not via .env

**Project structure:**
```
project-root/
├── .env                 # Environment file here
├── Cargo.toml
├── crates/
└── ui/
    ├── src/
    └── src-tauri/
        ├── Cargo.toml
        └── src/
            └── main.rs  # dotenvy loaded here
```

**Assumption (wrong):**
Since `main.rs` is in `ui/src-tauri/src/`, you might think CWD is `ui/src-tauri/`
and use `../../.env` to reach the project root.

**Reality:**
When `cargo tauri dev` runs, the working directory is the **project root**, not
`ui/src-tauri/`. So the path should just be `.env`.

## Solution

Try multiple paths to handle different execution contexts:

```rust
fn main() {
    // Load .env file - try multiple locations
    // When running via `cargo tauri dev`, CWD is project root
    // When running the binary directly, CWD varies
    let env_paths = [
        ".env",                    // Project root (cargo tauri dev)
        "../../.env",              // From ui/src-tauri (if run directly)
        "../.env",                 // From ui/ (if run from there)
    ];

    let mut loaded = false;
    for path in &env_paths {
        if dotenvy::from_filename(path).is_ok() {
            eprintln!("Loaded .env from: {}", path);
            loaded = true;
            break;
        }
    }

    if !loaded {
        eprintln!("Warning: Could not load .env file from any location");
    }

    tauri::Builder::default()
        // ... rest of setup
}
```

**Cargo.toml dependency:**
```toml
[dependencies]
dotenvy = "0.15"
```

## Verification

1. Add logging to see which path works:
   ```rust
   eprintln!("Loaded .env from: {}", path);
   ```

2. Check the Tauri dev output for the message:
   ```
   Loaded .env from: .env
   ```

3. Verify env vars are available:
   ```rust
   println!("GHOST_URL = {:?}", std::env::var("GHOST_URL"));
   ```

## Example

**Before (fails):**
```rust
fn main() {
    // Wrong - assumes CWD is ui/src-tauri
    if let Err(e) = dotenvy::from_filename("../../.env") {
        eprintln!("Warning: Could not load .env: {}", e);
    }
    // ...
}
```

**After (works):**
```rust
fn main() {
    // Correct - CWD is project root during cargo tauri dev
    if let Err(e) = dotenvy::from_filename(".env") {
        eprintln!("Warning: Could not load .env: {}", e);
    }
    // ...
}
```

## Notes

- The working directory behavior is determined by how Tauri's dev command runs cargo
- In production builds, the working directory may be different (app installation dir)
- For production, consider embedding secrets differently or using a config file
- The multi-path approach handles both dev and various execution scenarios
- Always log which path was loaded to aid debugging

## Related

- Tauri doesn't automatically load .env files - you must add dotenvy yourself
- This issue is separate from Tauri IPC (which only works in the webview)
- Environment variables set in the shell will override .env file values
