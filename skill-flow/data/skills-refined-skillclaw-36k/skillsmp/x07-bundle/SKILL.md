---
name: x07-bundle
description: Produce distributable native executables (normal CLI ABI) via `x07 bundle`.
metadata:
  short-description: Bundle native executables
  version: 0.1.0
  kind: docs
---

# x07-bundle

Use `x07 bundle` to produce a native executable that can be run directly on the target machine without the X07 toolchain installed at runtime.

`x07 bundle` runs the canonical auto-repair loop by default (`--repair=...`), so it can format/lint/apply quickfixes before compiling. Use `--repair=off` when debugging.

## Canonical commands

- Bundle an OS-world CLI executable:
  - `x07 bundle --project x07.json --profile os --out dist/app`
  - run it: `./dist/app --help`

- Bundle a policy-enforced OS-world executable:
  - `x07 bundle --project x07.json --profile sandbox --out dist/app`
  - requires a base policy (via `profiles.sandbox.policy` or `--policy`)

## Runtime ABI

The bundled executable:

- reads standard process args (`argc/argv`)
- encodes them into `argv_v1` input bytes
- calls the compiled program entrypoint (`x07_solve_v2`)
- writes program output bytes directly to stdout (no framing)

## Emit artifacts (debug / CI)

- `x07 bundle ... --emit-dir dist/emit`
  - emits `report.json`, `program.freestanding.c`, `wrapper.main.c`, and `bundle.combined.c`
  - for `run-os-sandboxed`, also emits `policy.used.json`

## Report contract

`x07 bundle` prints a machine JSON report to stdout:

- `schema_version: "x07.bundle.report@0.1.0"`
- `report` contains the underlying runner report used to compile the native artifact
