# Quick Reference

## Skill Structure

```
skill-name/
├── SKILL.md              # Required: frontmatter + instructions
├── scripts/              # Optional: executable code
├── references/           # Optional: reference docs (loaded on demand)
└── assets/               # Optional: templates, images (not loaded into context)
```

## SKILL.md Frontmatter

```yaml
---
name: my-skill
description: What it does and when to use it. This triggers the skill.
---
```

## Common Iteration Scenarios

| Problem | Solution |
|---------|----------|
| Claude rewrites same code | Add `scripts/` |
| Missing domain knowledge | Add `references/` |
| Inconsistent output | Add templates to SKILL.md |
| Wrong trigger conditions | Improve `description` |
| SKILL.md too long | Move content to `references/` |

## Key Principles

1. **Concise**: Only add what Claude doesn't already know
2. **Progressive disclosure**: SKILL.md < 500 lines, details in references
3. **No extra docs**: No README.md, CHANGELOG.md, etc.
