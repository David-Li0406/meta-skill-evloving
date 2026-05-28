---
name: writing-shell-scripts
description: >-
  Applies Bash style conventions when creating or editing shell scripts.
  Use when: (1) creating new shell scripts, (2) editing existing scripts in /bin/,
  or (3) reviewing Bash code for bugs or style issues.
---

# Bash Style Guide

Apply the Bash conventions from `./references/BASH.md` when creating or editing shell scripts.

## Key Conventions

Read `./references/BASH.md` for the complete guide. Summary:

### Script Structure

- Shebang: `#!/usr/bin/env bash`
- Strict mode: `set -euo pipefail`
- Main function called at end: `main "${@}"`

### Naming

- Functions: `snake_case`
- Local variables: `lower_case`
- Constants: `ALL_CAPS` with `readonly`

### Syntax

- Variable expansion: `${var}` not `$var`
- Command substitution: `$(...)` not backticks
- Tests: `[[...]]` not `[...]`
- Function syntax: `function name() { }` with both keyword and parentheses

### Quoting

- Always quote variable expansions: `"${var}"`
- Always quote command substitutions: `"$(cmd)"`
- Use arrays for lists, not word splitting

### Local Variables

- Declare with `local`
- Separate declaration from command substitution to preserve exit codes

## Validation

Whenever possible, validate the script before finishing. Prefer using a project-specific validation script, if available. Common locations include declarations in `package.json` and scripts stored in `bin/`. If those aren't present, `shellcheck` is a commonly available linter for shell scripts.
