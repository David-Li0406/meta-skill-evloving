---
name: skill-iterator
description: Guide for iterating and improving skills. Use when updating an existing skill that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
license: Complete terms in LICENSE.txt
---

# Skill Iterator

Guide for developing and iterating Claude Code Skills using the official skill-creator.

## Prerequisites: Install Official Skill Creator

Before developing or iterating skills, install the official `skill-creator` from Anthropic:

```bash
# Step 1: Add the skills marketplace
/plugin marketplace add anthropics/skills

# Step 2: Install example-skills (includes skill-creator)
/plugin install example-skills@anthropic-agent-skills
```

Official repo: https://github.com/anthropics/skills/tree/main/skills/skill-creator

## SOP: Skill Development Workflow

### Creating a New Skill

1. Invoke skill-creator:
   ```
   /example-skills:skill-creator
   ```
2. Follow the guided workflow to create the skill

### Iterating an Existing Skill

1. Invoke skill-creator:
   ```
   /example-skills:skill-creator
   ```
2. Point to the skill you want to modify
3. Make changes following skill-creator's guidance

**Important**: Always invoke `/example-skills:skill-creator` before making any skill modifications. The skill-creator provides the latest best practices and validation.

## Quick Reference

See [references/quick-ref.md](references/quick-ref.md) for skill structure and common patterns.
