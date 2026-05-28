---
name: canonical-targets
description: |
  Single source of truth for canonical VMs, canonical IDEs, and canonical trunk branch.
  Use this to keep dx-status, mcp-doctor, and setup scripts aligned across machines.
tags: [dx, ide, vm, canonical, targets]
allowed-tools:
  - Bash(scripts/canonical-targets.sh:*)
---

# Canonical Targets

Authoritative registry for:
- Canonical VM targets
- Canonical IDE set
- Canonical trunk branch (`master`)

## Usage

```bash
./scripts/canonical-targets.sh list
./scripts/canonical-targets.sh ide-config-path codex-cli
```

See `docs/CANONICAL_TARGETS.md` for the current canonical list and conventions.
