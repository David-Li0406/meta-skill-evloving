---
name: agent-skills-management
description: Use this skill when you need to create, modify, or validate Agent Skills following the agentskills.io specification.
---

# Agent Skills Management

This skill provides a comprehensive framework for creating, modifying, and validating Agent Skills that adhere to the agentskills.io specification. 

## When to Use This Skill

Use this skill when:
- You want to create a new Agent Skill from scratch.
- You need to modify or improve an existing Agent Skill.
- You want to validate the structure or content of a skill's `SKILL.md` file.
- You are reviewing the quality of skills before sharing them.
- You need to organize skill directories with proper naming and descriptions.

## Understanding Agent Skills

Agent Skills are modular packages that extend AI agent capabilities. Each skill is a directory containing a `SKILL.md` file with metadata and instructions.

### Progressive Disclosure Principle

Skills utilize progressive disclosure to manage context efficiently:
1. **Discovery**: At startup, agents load only the name and description.
2. **Activation**: When relevant, agents read the full `SKILL.md` instructions.
3. **Execution**: Agents load referenced files or execute code as needed.

This approach keeps agents responsive while providing access to more context on demand.

## SKILL.md Format

Every skill must start with YAML frontmatter followed by Markdown instructions.

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
metadata:
  author: your-name
  version: "1.0"
allowed-tools: Read, Grep, Glob # optional
---
```

### Name Field Specifications

- **Required**: Yes
- **Constraints**: 1-64 characters, lowercase letters/numbers/hyphens only
- Must match the parent directory name exactly.

**Valid Examples**:
- `pdf-processing`
- `data-analysis`

**Invalid Examples**:
- `PDF-Processing` (uppercase)
- `-pdf` (starts with hyphen)

## Common Mistakes

| Mistake                     | Fix                                       |
| --------------------------- | ----------------------------------------- |
| Not following naming rules  | Ensure name matches directory and follows constraints. |
| Overly verbose descriptions  | Keep descriptions concise and focused on triggers. |

## Process for Creating or Modifying Skills

1. **Check for Existing Skills**: Before creating a new skill, check if one already exists that meets your needs.
   ```bash
   # List all existing skills
   ls skills/*/
   ```

2. **Review Existing Skills**: Look for similar skills to avoid duplication and consider extending or improving them instead.

3. **Draft Your Skill**: Follow the SKILL.md format and ensure all required fields are filled out correctly.

4. **Validate Your Skill**: Use tools or manual checks to ensure your skill adheres to the agentskills.io specification.

5. **Share and Iterate**: Once validated, share your skill with others and be open to feedback for further improvements.

By following these guidelines, you can effectively manage Agent Skills and enhance the capabilities of AI agents.