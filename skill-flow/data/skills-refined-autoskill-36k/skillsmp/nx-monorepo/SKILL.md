---
name: nx-monorepo
description: Nx workspace layout detection and file layout guidance.
---

# Nx Monorepo Layout Detection

## Detection

Check for `nx.json` in the repository root:

- If present: Nx workspace layout.
- If absent: Standard layout.

## Layout

### Nx Workspace

- `apps/<app-name>/src/`
- `libs/<lib-name>/src/`

### Standard Layout

Frontend:

- `src/app/`
- `src/components/`

Backend (Go):

- `cmd/<app>/`
- `internal/`
- `pkg/`

Backend (Rust):

- `src/main.rs`
- `src/lib.rs`

## Usage

Detect layout before generating file paths or imports.
