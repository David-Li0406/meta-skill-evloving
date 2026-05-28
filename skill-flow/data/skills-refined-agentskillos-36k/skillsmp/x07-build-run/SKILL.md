---
name: x07-build-run
description: Expert backend for deterministic solve-world execution via x07-host-runner. Prefer `x07 run` as the canonical agent entry point.
metadata:
  short-description: Compile + run (solve worlds)
  version: 0.1.0
  kind: docs
---

# x07-build-run

Prefer `x07 run` for normal execution. Use `x07-host-runner` directly only when you need host-runner-specific flags (fixtures, explicit compiled artifact paths, debug toggles) or when you are debugging runner behavior.

This skill documents both:

- **Canonical (recommended):** `x07 run ...` (single front door for agents)
- **Expert backend:** `x07-host-runner ...`

## Canonical commands (recommended: `x07 run`)

- Run the current project (auto-discovers `x07.json` when present):
  - `x07 run`

- Run a single program (solve-pure):
  - `x07 run --program src/main.x07.json --world solve-pure`

- Provide binary stdin:
  - `x07 run --program src/main.x07.json --world solve-pure --input input.bin`

- Compile only (no execution):
  - `x07 run --program src/main.x07.json --world solve-pure --compile-only`

## Expert backend commands (`x07-host-runner`)

- Run a single program (solve-pure):
  - `x07-host-runner --program src/main.x07.json --world solve-pure --module-root src`

- Run a project (uses `x07.json` + `x07.lock.json`):
  - `x07-host-runner --project x07.json`

- Provide binary stdin:
  - `x07-host-runner --program src/main.x07.json --world solve-pure --module-root src --input input.bin`

- Compile only (no execution):
  - `x07-host-runner --program src/main.x07.json --world solve-pure --module-root src --compile-only`

## Output contract

- `x07 run` in `solve-*` worlds prints an `x07-host-runner.report@...` JSON report to stdout (pass-through).
- `x07-host-runner` prints the same report shape when invoked directly.

In both cases:
- Use the process exit code for pass/fail.
- Parse the JSON for `schema_version`, `mode`, and base64-encoded output bytes.
