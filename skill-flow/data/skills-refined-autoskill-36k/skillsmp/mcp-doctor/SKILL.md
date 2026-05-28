---
name: mcp-doctor
description: |
  Warn-only health check for canonical MCP configuration and related DX tooling.
  Strict mode is opt-in via MCP_DOCTOR_STRICT=1.
tags: [dx, mcp, health, verification]
allowed-tools:
  - Bash(mcp-doctor/check.sh:*)
---

# mcp-doctor

Runs a fast, safe verification of canonical MCP + DX expectations.

## Usage

```bash
~/agent-skills/mcp-doctor/check.sh
MCP_DOCTOR_STRICT=1 ~/agent-skills/mcp-doctor/check.sh
```

## Design

- Warn-only by default (never blocks automation unless strict mode is enabled).
- Never prints secrets.
- Checks canonical IDE config locations (see `docs/CANONICAL_TARGETS.md`).
