---
name: cli
description: Guidelines for designing and documenting Command Line Interfaces.
---

# CLI

## Design Interface
Design top-level commands that categorize actions, followed by imperative subcommands (similar to `kubectl`):

```bash
./announce slack post --channel "#foo"
```

## Document CLI
Ensure the CLI is self-documenting:
- **Help Flags**: All commands and subcommands must describe their function via `--help`, ideally with examples.
- **Man Pages**: For complex applications, generate or provide a comprehensive `man` page.
