# Skill Anatomy & Progressive Disclosure

Understanding how skills are loaded and used.

## Skill Directory Structure

```
skill-name/
├── SKILL.md          # Required: frontmatter + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: detailed docs (loaded on-demand)
├── templates/        # Optional: starter files for output
└── assets/           # Optional: images, fonts, binary files
```

## SKILL.md Structure

```yaml
---
# YAML Frontmatter (required)
name: skill-name          # Required: lowercase, hyphens, ≤64 chars
description: ...          # Required: what + when, ≤1024 chars
license: MIT              # Optional: license name or file
requirements: ...         # Optional: environment hints, ≤500 chars
metadata:                 # Optional: arbitrary key-value pairs
  version: "1.0"
  author: your-name
---

# Markdown Body (required)
[Instructions, examples, guidelines]
```

## Progressive Disclosure Levels

### Level 1: Discovery (Always Loaded)
- Only `name` and `description` from frontmatter
- Used to decide if skill is relevant
- Costs tokens for EVERY installed skill

**Implication**: Write great descriptions. They're always in context.

### Level 2: Activation (Loaded When Relevant)
- Full SKILL.md body
- Triggered when Claude decides the skill matches the task
- Costs tokens only when skill is used

**Implication**: Keep SKILL.md focused. It's the "core manual."

### Level 3: Deep Dive (Loaded On-Demand)
- Files in references/, scripts/, etc.
- Claude reads specific files as needed
- Costs tokens only when that specific file is accessed

**Implication**: Move detailed content here. It's "free" until needed.

## Loading Flow

```
User Request
    │
    ▼
┌─────────────────────────────┐
│  Check skill descriptions   │  ← Level 1 (always in context)
│  (name + description only)  │
└─────────────────────────────┘
    │
    ▼ (if relevant)
┌─────────────────────────────┐
│  Read full SKILL.md body    │  ← Level 2 (loaded now)
└─────────────────────────────┘
    │
    ▼ (if needed)
┌─────────────────────────────┐
│  Read specific reference    │  ← Level 3 (loaded now)
│  or run specific script     │
└─────────────────────────────┘
    │
    ▼
Execute Task with Loaded Context
```

## Scripts vs. References

| Type | Purpose | How Claude Uses |
|------|---------|-----------------|
| **scripts/** | Executable code | Runs via bash, only output enters context |
| **references/** | Documentation | Reads into context when needed |
| **assets/** | Output resources | Copies/uses in generated output |

### When to Use Scripts
- Deterministic operations (sorting, validation, parsing)
- Operations that would be expensive via tokens
- Repeatable workflows that must be consistent

### When to Use References
- Detailed documentation
- Schema definitions
- Domain-specific knowledge
- Examples and templates

## Referencing Files

From SKILL.md, use relative paths:

```markdown
For detailed API documentation, see [references/API.md](references/API.md).

To validate the schema, run:
```bash
python scripts/validate.py input.json
```
```

Claude will read the referenced file only when it needs that information.

## Token Efficiency

| Content | Token Cost |
|---------|------------|
| Skill metadata (name, description) | Always |
| SKILL.md body | Only when skill is used |
| Reference files | Only when specifically read |
| Script code | Never (only output costs tokens) |
| Script output | When script is run |

**Key insight**: Scripts are maximally efficient. Their code never enters context—only their output does.

## Source Attribution

This document synthesizes information from:
- [Agent Skills Standard](https://agentskills.io)
- [Anthropic Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [VS Code Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
