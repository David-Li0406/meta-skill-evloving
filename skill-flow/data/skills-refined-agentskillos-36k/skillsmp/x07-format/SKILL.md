---
name: x07-format
description: Canonically format X07 x07AST JSON files using `x07 fmt` (check/write) with a machine-readable JSON report.
metadata:
  short-description: Format x07AST JSON
  version: 0.1.0
  kind: docs
---

# x07-format

Use this skill to keep x07AST JSON canonical (stable ordering + trailing newline).

## Canonical commands

- Check a file:
  - `x07 fmt --input src/main.x07.json --check --report-json`

- Rewrite a file:
  - `x07 fmt --input src/main.x07.json --write --report-json`

## Notes

- `x07 fmt` requires exactly one of `--check` or `--write`.
- In `--check` mode, exit code `1` means the file would change.
