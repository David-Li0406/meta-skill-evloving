---
name: bootstrap-monorepo
description: Autonomous polyglot monorepo bootstrap meta-prompt. TRIGGERS - new monorepo, polyglot setup, scaffold Python+Rust+Bun, monorepo from scratch.
allowed-tools: Read
---

# Bootstrap Polyglot Monorepo

This skill redirects to the canonical reference in mise-tasks.

→ **See**: [mise-tasks/references/bootstrap-monorepo.md](../mise-tasks/references/bootstrap-monorepo.md)

## When to Use

- Starting a new polyglot monorepo from scratch
- Setting up Python + Rust + Bun/TypeScript project structure
- Need autonomous 9-phase bootstrap workflow (includes release setup)
- Want Pants + mise integration for affected detection

## Stack

| Tool      | Responsibility                                                         |
| --------- | ---------------------------------------------------------------------- |
| **mise**  | Runtime versions (Python, Node, Rust) + environment variables          |
| **Pants** | Build orchestration + native affected detection + dependency inference |

## Quick Commands

```bash
# After bootstrap, use these Pants commands:
pants --changed-since=origin/main test    # Test affected
pants --changed-since=origin/main lint    # Lint affected
pants tailor                               # Generate BUILD files
pants list ::                              # List all targets
```

## Related Skills

- `itp:mise-tasks` - Task orchestration and affected detection (Level 11)
- `itp:mise-configuration` - Environment and tool version management
- `itp:semantic-release` - Release automation (Phase 8 reference)
