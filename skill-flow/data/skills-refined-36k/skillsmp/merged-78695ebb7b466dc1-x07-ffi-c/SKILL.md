---
name: x07-ffi-c
description: Use this skill when embedding an X07 program as a library in C/C++.
---

# x07-ffi-c

Use this skill when embedding an X07 program as a library.

## Canonical commands

- Emit C + header from a program file:
  - `x07c compile --program <input_file> --world <world_name> --module-root <module_root> --out <output_c_file> --emit-c-header <output_header_file>`

- Emit C + header from a project manifest:
  - `x07c build --project <project_file> --out <output_c_file> --emit-c-header <output_header_file>`

## Notes

- `--emit-c-header` disables emitting a `main` entrypoint, so the output is linkable/embeddable.