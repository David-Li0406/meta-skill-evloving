---
name: agent-skills-management
description: Use this skill when creating, modifying, or reviewing Agent Skills following the agentskills.io specification.
---

# Agent Skills Management

This skill provides comprehensive guidance for creating, validating, and managing Agent Skills that adhere to the agentskills.io specification.

## When to Use This Skill

Use this skill when:
- You need to create a new Agent Skill.
- You want to modify or improve an existing skill.
- You need to validate a skill's structure or frontmatter.
- You are reviewing skill quality before sharing.
- You want to understand the Agent Skills format and best practices.

## What Are Agent Skills?

Agent Skills are modular packages that extend AI agent capabilities with specialized knowledge and workflows. Each skill is a directory containing a `SKILL.md` file with metadata and instructions.

### Progressive Disclosure Principle

Skills utilize progressive disclosure to manage context efficiently:
1. **Discovery**: At startup, agents load only the name and description.
2. **Activation**: When relevant, agents read the full SKILL.md instructions.
3. **Execution**: Agents load referenced files or execute code as needed.

## Directory Structure

```
skill-name/
├── SKILL.md          # Required: instructions + metadata
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
└── assets/           # Optional: templates, resources
```

## SKILL.md Format

Every skill starts with YAML frontmatter followed by Markdown instructions.

### Required Frontmatter

```yaml
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

### Optional Frontmatter Fields

```yaml
---
name: skill-name
description: What this skill does and when to use it.
license: MIT
compatibility: Requires specific tools or environment
metadata:
  author: example-org
  version: "1.0"
allowed-tools: Bash(git:*) Bash(jq:*) Read
---
```

## Body Content Guidelines

The Markdown body after frontmatter contains the skill instructions. Follow these best practices:

### Recommended Sections

1. **When to Use This Skill** - Clear triggers for when agents should activate this skill.
2. **What This Skill Does** - Brief overview of capabilities.
3. **Step-by-Step Instructions** - Detailed procedures.
4. **Examples** - Sample inputs and expected outputs.
5. **Common Patterns** - Reusable approaches.
6. **Best Practices** - Tips and recommendations.
7. **Edge Cases** - How to handle unusual situations.

### Content Best Practices

- Keep main SKILL.md under 500 lines.
- Use clear, actionable language.
- Include code examples where helpful.
- Focus on the "why" and "how", not just "what".

## Validation Checklist

Before finalizing a skill, verify:

- [ ] Directory name matches `name` in frontmatter.
- [ ] `name` is 1-64 chars, lowercase alphanumeric + hyphens only.
- [ ] `description` is 1-1024 chars and includes when to use.
- [ ] YAML frontmatter is valid.
- [ ] Main SKILL.md is under 500 lines.
- [ ] File references use relative paths.

## Common Anti-Patterns

- **Vague Descriptions**: Ensure descriptions are specific and include activation triggers.
- **Over-Explaining Common Knowledge**: Avoid explaining concepts agents already know.
- **Deeply Nested References**: Keep references one level deep from SKILL.md.

## Example Skill Template

```markdown
---
name: example-skill
description: Brief description of what this does and when to use it.
---

## When to Use This Skill
Use when...

## Instructions
1. Step one
2. Step two
3. Step three
```

## Resources

For more information:
- [agentskills.io specification](https://agentskills.io/specification)
- [Integration guide](https://agentskills.io/integrate-skills)
- [Example skills on GitHub](https://github.com/anthropics/skills)
- [Authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)