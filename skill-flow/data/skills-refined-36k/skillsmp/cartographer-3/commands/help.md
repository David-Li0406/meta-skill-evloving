---
model: haiku
allowed-tools: Read
description: Display Cartographer usage guide and workflow documentation
---

## Cartographer Help

Print the following help documentation:

```markdown
# Cartographer Plugin

Generate AI-optimized codebase navigation (`/atlas` skills) plus spec-driven development workflows.

## Quick Start

1. **Generate atlas:** `/cartographer:chart`
2. **Use atlas:** `/atlas` (auto-invoked when asking "where is X?")
3. **Keep fresh:** `/cartographer:health` → `/cartographer:rechart`

## Commands

### Atlas Generation
| Command | Description |
|---------|-------------|
| `/cartographer:chart` | Generate complete atlas (initial) |
| `/cartographer:rechart` | Update atlas incrementally |
| `/cartographer:orient` | Add atlas reference to CLAUDE.md |
| `/cartographer:embed` | Export for plugin-free use |

### Atlas Health
| Command | Description |
|---------|-------------|
| `/cartographer:health` | Check drift, structure, and quality |
| `/cartographer:health --drift-only` | Only check drift |
| `/cartographer:health --structure-only` | Only check structure |
| `/cartographer:health --fix` | Auto-fix simple issues |

### Atlas Usage
| Command | Description |
|---------|-------------|
| `/cartographer:where <query>` | Quick path lookup |
| `/cartographer:explore <domain>` | Enrich domain docs |
| `/cartographer:capture` | Add patterns/anti-patterns |

### Navigator (Spec-Driven Development)
| Command | Description |
|---------|-------------|
| `/navigator:plan <task>` | Create spec with atlas context |
| `/navigator:build <spec>` | Execute spec with patterns |
| `/navigator:review <spec>` | Review with agents (default) |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Atlas not found | `/cartographer:chart` |
| Atlas stale | `/cartographer:health` then `/cartographer:rechart` |
| Wrong project type | Re-run `/cartographer:chart` with context |
| Navigator blocked | Ensure atlas exists |
| Generic anti-patterns | `/cartographer:health --fix` |
| Incomplete patterns | `/cartographer:explore --pattern <id>` |

## More Info

- Reference docs: `cartographer/references/`
- Templates: `cartographer/assets/atlas-templates/`
```
