---
name: workflow-env
description: Global workflow rule that enforces sourcing env.sh (if present) before running build, run, or deployment commands.
---

# Environment Loading Protocol

## Rule

Before any build/run/deploy command, check for `env.sh`:

1. **If present**: Source it, then run the command.
   - Syntax: `. ./env.sh && <command>`
2. **If absent**: Run the command normally.

## Applies To

- Node: `pnpm`, `bun` scripts (`dev`, `build`, `start`)
- Compilers: `zig`, `go`, `cargo`, `dotnet`
- Task runners: `make`, `just`, `rake`
- Infra: `docker`, `docker-compose`, `terraform`, `kubectl`

## Example

```bash
. ./env.sh && pnpm build
```
