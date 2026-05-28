---
name: skill-creation-guide
description: Use this skill when you need to create and manage Claude Code skills effectively, following best practices and structured documentation.
---

# Skill Creation Guide

This skill provides a comprehensive framework for creating new Claude Code skills, ensuring they are well-structured, documented, and maintainable.

## When to Use

- "Create a skill for X"
- "Help me make a new skill"
- "Turn this script into a skill"
- "How do I create a skill?"

## Skill Structure

Skills are organized in the following directory structure:

```
.claude/skills/<skill-name>/
├── SKILL.md          # Required: Main skill definition
├── scripts/          # Optional: Supporting scripts
└── templates/        # Optional: Templates, examples
```

### SKILL.md Format

```yaml
---
name: skill-name
description: Brief description (shown in skill list)
version: 1.0.0
allowed-tools: [Bash, Read, Write]  # Optional: restrict tools
---

# Skill Name

## Purpose
[2-3 sentences explaining what this skill helps accomplish and why it matters]

## When to Use This Skill
- [Specific scenario 1]
- [Specific scenario 2]
- [Specific scenario 3]

## Instructions

1. **Greeting**: Welcome the user and introduce the skill's purpose.
2. **Explain Structure**: Describe the SKILL.md format and its components.
3. **Demonstrate Tool Usage**: Show how to use the allowed tools effectively.

### Example Invocation

```
User: "Use the skill-name"

Response:
👋 Hello! I'm the skill-name, designed to help you with [brief description of functionality].
```

## Best Practices

- **Clear Structure**: Organize content into logical sections.
- **YAML Frontmatter**: Use proper metadata format.
- **Documentation**: Include comments and explanations for clarity.
- **Testing and Maintenance**: Ensure skills are testable and maintainable.

## Creation Checklist

### Before Creating

- [ ] Does a similar skill already exist?
- [ ] Is this knowledge needed repeatedly (3+ times)?
- [ ] Is there enough depth for a skill (500+ words)?
- [ ] Does it apply across multiple contexts?

### Structure Quality

- [ ] Clear, descriptive name (kebab-case)
- [ ] Accurate one-line description
- [ ] Comprehensive purpose section
- [ ] "When to Use" with specific scenarios
- [ ] Code examples that actually work
```