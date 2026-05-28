---
name: ast-grep
description: "Read-only structural code search with ast-grep/sg. Grep/rg/sed alternative for AST-aware CLI exploration, pattern search, and fast code discovery. Activates on ast-grep/sg, structural search, AST search, find usages, tree-sitter."
---

# ast-grep

## Overview
Read-only CLI search with `sg` or `ast-grep`. AST-aware grep for code exploration and SWE tasks.

## Quick start
- Prefer `sg`. Fallback `ast-grep`. Last resort: `nix run nixpkgs#ast-grep --`.
- Basic pattern search:
  - `sg -p 'console.log($MSG)' -l ts src`
- Files with matches only:
  - `sg -p 'console.log($$$)' -l ts --files-with-matches src`
- Show JSON (stream):
  - `sg -p 'console.log($$$)' -l ts --json=stream src`

## Workflow
- Locate: start with narrow paths + `--globs` include/exclude.
- Verify language: set `-l/--lang` for stdin or ambiguous files.
- Inspect: use `--debug-query` or `--inspect summary` when matches surprise.
- Report: `--files-with-matches` or `--json=stream` for pipelines.
 - Prefer read-only search; skip rewrite flags.

## Tasks
- Pattern search: `run` (default) with `-p/--pattern`.
- Context: `-A/-B/-C` for line context.
- Performance: narrow paths, `--globs`, `--files-with-matches`, `--json=stream`.

## Guardrails
- Read-only: never use `--rewrite`, `-r`, `--update-all`, or `--interactive`.
- Stdin requires `--lang`.

## Resources
- `reference.md`: patterns, strictness, selectors, output formats.
- `cookbook/`: practical recipes.
