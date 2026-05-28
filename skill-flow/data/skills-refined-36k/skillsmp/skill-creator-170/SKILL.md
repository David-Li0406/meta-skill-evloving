---
name: skill-creator
description: Create new OpenCode skills with proper structure and best practices
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: meta
---

# Skill Creator

Create effective OpenCode skills that extend AI capabilities with specialized knowledge, workflows, and tool integrations.

## When to Use

- Creating a new skill for a repeatable workflow
- Converting documentation into a skill
- Packaging domain expertise for reuse
- Building team-specific automation

## Skill Structure

```
skill-name/
├── SKILL.md          # Required - main instructions
├── scripts/          # Optional - executable code
├── references/       # Optional - loaded as context
└── assets/           # Optional - files used in output
```

## SKILL.md Template

```markdown
---
name: skill-name
description: One-line description of when to use this skill
license: MIT
compatibility: opencode
metadata:
  audience: developers|users|teams
  workflow: development|productivity|automation
---

# Skill Name

Brief overview of what this skill does.

## When to Use

- Specific trigger 1
- Specific trigger 2
- Specific trigger 3

## How to Use

Step-by-step instructions...

## Examples

Real usage examples...
```

## Writing Guidelines

### 1. Clear Triggers
The `description` field determines when the skill activates. Be specific:
- Good: "Generate changelog from git commits for release notes"
- Bad: "Help with changelogs"

### 2. Imperative Instructions
Write as commands, not suggestions:
- Good: "Run `git log` to fetch commits"
- Bad: "You should probably check the git log"

### 3. Progressive Disclosure
- SKILL.md: Core workflow (always loaded)
- references/: Deep details (loaded when needed)
- scripts/: Automation (executed on demand)

### 4. Concrete Examples
Start with real use cases:
```
## Example

**Input**: "Create changelog for v2.0"

**Output**:
## v2.0.0 - 2025-01-15

### Features
- Add dark mode support
- Implement user preferences

### Fixes
- Resolve memory leak in cache
```

## Creation Process

1. **Identify the pattern**: What task do you repeat?
2. **Gather examples**: Collect 3-5 real instances
3. **Extract the workflow**: What steps are always the same?
4. **Write SKILL.md**: Document the procedure
5. **Add resources**: Scripts, references, assets as needed
6. **Test and iterate**: Use it, improve it

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Vague descriptions | Won't trigger correctly | Be specific about use cases |
| Duplicate info | Confuses context | Single source of truth |
| Overly long SKILL.md | Slow to load | Use references/ for deep details |
| No examples | Hard to understand | Always include real examples |

## Validation Checklist

Before publishing:
- [ ] Name is lowercase-kebab-case
- [ ] Description explains WHEN to use (not WHAT it does)
- [ ] Instructions are imperative, not suggestive
- [ ] At least one concrete example included
- [ ] No duplicate information across files
- [ ] Tested with real use cases
