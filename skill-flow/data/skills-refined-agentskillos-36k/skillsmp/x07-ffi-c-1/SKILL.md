---
name: x07-ffi-c
description: Emit C output and a C header for embedding X07 in C/C++ via x07c --emit-c-header.
metadata:
  short-description: Emit C + header
  version: 0.1.0
  kind: docs
---

# x07-ffi-c

Use this skill when embedding an X07 program as a library.

## Canonical commands

- Emit C + header from a program file:
  - `x07c compile --program src/main.x07.json --world solve-pure --module-root src --out target/out.c --emit-c-header target/out.h`

- Emit C + header from a project manifest:
  - `x07c build --project x07.json --out target/out.c --emit-c-header target/out.h`

## Notes

- `--emit-c-header` disables emitting a `main` entrypoint, so the output is linkable/embeddable.
