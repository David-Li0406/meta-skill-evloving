---
name: docs
version: 1.0.0
changelog: Initial docs generator for skill table
description: Update README.md commands table from skills.
---

# Docs

Update README.md commands table from skills.

## Task
$ARGUMENTS

## Instructions

Output: `## Docs`

**State**: Utility command. Does not modify STATE.md phase.

### 1. Scan Skills

Read all files in `.claude/skills/*/SKILL.md` and extract:
- Skill name (directory name)
- Description (first non-heading, non-frontmatter line)

### 2. Generate Table

Format as markdown table:

```markdown
| Command | Description |
|---------|-------------|
| `/skill-name` | First line description |
```

Sort alphabetically by skill name.

### 3. Update README

Replace content between markers in README.md:

```
<!-- COMMANDS:START -->
[generated table]
<!-- COMMANDS:END -->
```

### 4. Report

Show the updated commands table.

## Constraints

- Only update the section between markers
- Preserve all other README content
- Don't add skills that don't have SKILL.md

## Exit Criteria

README.md commands section updated with current skills.
