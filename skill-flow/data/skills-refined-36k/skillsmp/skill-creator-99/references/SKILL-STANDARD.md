# Agent Skills Standard

Agent Skills follow a strict standard so the AI always has the context needed to behave like a domain expert.

## Skill Structure

Every skill lives under `skills/` and must include:

1. `SKILL.md`: Main instruction file with YAML frontmatter.
2. `references/`: Extended documentation (Markdown, diagrams, etc.).
3. `assets/`: Scripts, templates, or static resources.

## SKILL.md Format

### Required Frontmatter

```yaml
---
name: skill-name
description: Short description of what it does and when to invoke it.
license: MIT
metadata:
  author: GGA Team
  version: "1.0"
  scope: [root, api, backend, frontend]
  auto_invoke:
    - "keyword1"
    - "keyword2"
allowed-tools: [Read, Edit, Write, Glob, Grep, Bash]
---
```

### Required Sections

- **## When to Use It**: Clear usage scenarios.
- **## Critical Patterns**: Non-negotiable rules (ALWAYS/NEVER).
- **## Commands (optional)**: Frequent commands.
- **## Related Skills**: Links to related skills.
- **## Resources**: References to files under `references/`.
