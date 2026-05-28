---
name: skill-creator
description: Use when creating or editing skills for the ai-coding-config repository - it provides guidelines for writing effective and reusable skills.
---

# Skill Creator

## Overview

This skill serves as a guide for creating and editing skills that act as reusable reference materials for proven techniques, patterns, and tools. It emphasizes writing in a way that is focused on goals and outcomes rather than rigid procedures.

## When to Use

Use this skill when you need to create skills for techniques that are not intuitively obvious, patterns that are applicable across multiple projects, or broadly useful approaches. Avoid using this skill for one-off solutions, well-documented standard practices, or project-specific conventions.

## Core Pattern

Every skill should follow this structure:

```markdown
---
name: skill-name-with-hyphens
description: Use when [triggering conditions] - [what it does and how it helps]
---

# Skill Name

## Overview

What is this? Core principle in 1-2 sentences.

## When to Use

Clear triggers and symptoms. When NOT to use.

## Core Pattern

Show desired approach with examples. Describe alternatives in prose.

## Common Pitfalls

What goes wrong and how to avoid it.
```

### Frontmatter Requirements

- **name**: Use letters, numbers, and hyphens only. Use verb-first active voice (e.g., creating-skills, not skill-creation).
- **description**: Start with "Use when..." to describe triggering conditions, then explain what it does. Keep it under 500 characters and include concrete symptoms and situations.

### Writing Principles

- **Show, don't tell**: Demonstrate desired approaches with multiple examples and describe undesired alternatives in prose.
  
  Good pattern example:
  
  ```typescript
  // Use condition-based waiting for reliable async tests
  await waitFor(() => element.textContent === "loaded");
  await waitFor(() => user.isAuthenticated === true);
  await waitFor(() => data.length > 0);
  ```

  In prose: "Avoid arbitrary timeouts like setTimeout() which make tests brittle and slow."

- **Focus on goals, not process**: Describe outcomes and constraints, allowing the LLM to determine how to achieve them.