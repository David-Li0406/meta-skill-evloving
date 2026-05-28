---
name: agent-skills-creator
description: Use this skill when creating, validating, or modifying Agent Skills following the agentskills.io specification.
---

# Agent Skills Creator

A comprehensive skill for creating, validating, and managing Agent Skills that follow the agentskills.io specification.

## When to use this skill

Use this skill when:
- A user asks to create a new agent skill.
- A user wants to modify or improve an existing skill.
- A user needs to validate a skill's structure or frontmatter.
- A user mentions "skill", "agent skill", or agentskills.io.
- A user wants to understand the Agent Skills format.

## What Agent Skills are

Agent Skills are a lightweight, open format for extending AI agent capabilities with specialized knowledge and workflows. At its core, a skill is a folder containing a `SKILL.md` file with metadata and instructions.

### Progressive Disclosure Principle

Skills use progressive disclosure to manage context efficiently:
1. **Discovery**: At startup, agents load only name and description.
2. **Activation**: When relevant, agents read the full SKILL.md instructions.
3. **Execution**: Agents load referenced files or execute code as needed.

This keeps agents fast while providing access to more context on demand.

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
allowed-tools: Read, Grep, Glob
---
```

## Field Specifications

### Name Field
- **Required**: Yes
- **Constraints**: 1-64 characters, lowercase letters/numbers/hyphens only.
- Must not start or end with hyphen.
- Must not contain consecutive hyphens (`--`).
- Must match the parent directory name.

### Description Field
- **Required**: Yes
- **Constraints**: 1-1024 characters, non-empty.
- Should describe both what the skill does AND when to use it.
- Include specific keywords that help agents identify relevant tasks.

## Body Content Guidelines

The Markdown body after frontmatter contains the skill instructions. No format restrictions, but follow these best practices:

### Recommended Sections

1. **When to use this skill** - Clear triggers for when agents should activate this skill.
2. **What this skill does** - Brief overview of capabilities.
3. **Step-by-step instructions** - Detailed procedures.
4. **Examples** - Sample inputs and expected outputs.
5. **Common patterns** - Reusable approaches.
6. **Best practices** - Tips and recommendations.
7. **Edge cases** - How to handle unusual situations.

### Content Best Practices

- Keep main SKILL.md under 500 lines (< 5000 tokens recommended).
- Move detailed reference material to separate files in `references/`.
- Use clear, actionable language.
- Include code examples where helpful.
- Focus on the "why" and "how", not just "what".
- Consider the agent's perspective when writing instructions.

## Validation Checklist

Before finalizing a skill, verify:

- [ ] Directory name matches `name` in frontmatter.
- [ ] `name` is 1-64 chars, lowercase alphanumeric + hyphens only.
- [ ] `description` is 1-1024 chars and includes when to use.
- [ ] YAML frontmatter is valid.
- [ ] Main SKILL.md is under 500 lines.
- [ ] File references use relative paths.

## Example Skill Templates

### Minimal Skill
```markdown
---
name: example-skill
description: Brief description of what this does and when to use it.
---

## When to use this skill
Use when...

## Instructions
1. Step one
2. Step two
3. Step three
```

### Full-featured Skill
```markdown
---
name: advanced-skill
description: Comprehensive description with keywords for activation.
license: MIT
compatibility: Requires specific tools or environment
metadata:
  author: your-name
  version: "1.0"
---

## When to use this skill
Use when...

## What this skill does
Overview...

## Instructions
Detailed steps...

## Examples
Sample code and outputs...

## Best practices
Tips and recommendations...
```

## Remember

- **Specific beats generic** - In naming and content.
- **Trigger words matter** - Include terms users naturally mention.
- **One skill, one job** - Focus trumps comprehensiveness.
- **Token efficiency** - Every line earns its place.
- **Test activation** - Verify the skill loads when expected.

Skills are prompt engineering at scale. Make every word count.