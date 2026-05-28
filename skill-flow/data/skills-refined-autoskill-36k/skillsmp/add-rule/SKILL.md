---
name: add-rule
description: Add a new rule to the learned rules file
allowed-tools: Read, Edit
argument-hint: <rule-description>
---

# Add Rule

Add a new rule or guideline to the learned rules file.

## Instructions

1. Parse the argument provided by the user as the rule to add
2. Read the current `.claude/rules/learned.md` file
3. Determine the appropriate category for the rule (or create a new one)
4. Append the rule to the appropriate section
5. Confirm the addition to the user

## Categories

Common categories include:
- **User Preferences** - Personal workflow preferences
- **Code Style** - Formatting and style rules
- **Commands** - Specific command patterns to remember
- **Workflows** - Multi-step processes
- **Safety** - Additional safety rules

## Example Usage

User: `/add-rule Always use pnpm instead of npm in this project`

Result: Adds to User Preferences section:
```markdown
## User Preferences
- Always use pnpm instead of npm in this project
```

## Important

- Keep rules concise and actionable
- Avoid duplicating rules already in baseline.md
- Use clear, imperative language
