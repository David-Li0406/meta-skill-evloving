# Instruction File Templates

## Minimal Template

```markdown
---
description: 'Brief description of purpose'
applyTo: '**/*.ext'
---

# [Instruction Title]

## Overview
Brief introduction and context.

## Workflow
1. Step 1: Analyze the input.
2. Step 2: Execute the [Skill Name](skills/<skill-name>/SKILL.md).
3. Step 3: Verify the output.

## Rules & Constraints
- Rule 1
- Rule 2

## Best Practices

- Specific practice 1
- Specific practice 2

## Code Standards

### Naming Conventions
- Rule 1
- Rule 2

## Common Patterns

### Pattern 1
Description and example

```language
code example
```

## Validation

- Build command: `command to verify`
- Linting: `command to lint`
- Testing: `command to test`
```

## Frontmatter Only

```yaml
---
description: 'Brief description of the instruction purpose and scope'
applyTo: 'glob pattern for target files (e.g., **/*.ts, **/*.py)'
---
```
