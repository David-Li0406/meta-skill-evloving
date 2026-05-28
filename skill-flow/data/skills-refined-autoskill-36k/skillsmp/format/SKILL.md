---
name: format
description: Run code formatter on the codebase.
---

# Format

Run code formatters to automatically fix code style.

## Steps

1. Detect the project type and find the format command:
   - Nix with treefmt: `nix fmt`
   - TypeScript/JavaScript: `prettier --write`, `biome format --write`
   - Go: `gofmt -w`, `goimports -w`
   - Rust: `cargo fmt`
   - Python: `black`, `ruff format`

2. If treefmt is configured in the project, prefer `nix fmt` as it handles all formatters.

3. If no formatter is configured, propose adding one appropriate for the project.

4. Run the command to format the code.
