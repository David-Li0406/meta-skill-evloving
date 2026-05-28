---
name: create-skill
description: Expertly authors new agent skill by following strict standardization and template guidelines.
---

# Create SKILL.md

This skill create high-quality, reliable, and safe Skill for agents. When a user asks you to "create a skill" or "teach the agent how to [X]," you must follow the procedure below.

## Instructions

1.  **Analyze Intent:** Determine the *Trigger* (when the skill runs) and the *Action* (what it actually does).
2.  **Identify Tools:** Determine which CLI commands or MCP tools the skill needs (e.g., `grep`, `npm test`, `git status`).
3.  **Define Constraints:** What should the agent *never* do? (e.g., "Never delete data," "Never commit to main").
4.  **Name the Skill:** Give the directory a name that matches the *Trigger* and *Action* of the skill (e.g `grep-for-file`) and place the `SKILL.md` under that directory. 
5.  **Create SKILLS.md:** Output the full `SKILL.md` content inside a code block using the **Standard Template** below.
6.  **Create Optional Files:** If you need to include any additional files, such as scripts, assets, or references, place them in the sub-directories.


### Directory Structure
```
~/.config/ai/skills/{Skill Name}/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
├── scripts/          - (Optional) Executable code (Python/Bash/etc.)
├── references/       - (Optional) Documentation intended to be loaded into context as needed
└── assets/           - (Optional) Files used in output (templates, icons, fonts, etc.)
```

### Template

Refer to this structure for the `SKILL.md` file.

```markdown
---
name: [skill-name-kebab-case]
description: [One sentence summary of what this skill achieves]
---

# [Skill Name]

[Brief Context: Explain what this skill should do]

## When to Use this Skill
This skill is activated when the user asks to:

- [Trigger 1]
- [Trigger 2]

## Instructions
When this skill is active, strictly follow these steps in order:

1.  **[Step Name]**: [Instruction]
    - *Command:* `[Optional CLI command to run]`
2.  **[Step Name]**: [Instruction]
3.  **[Step Name]**: [Instruction]

## Critical Constraints (The "Guardrails")
-   **NEVER** [Constraint 1]
-   **ALWAYS** [Constraint 2]
- ⚠️ **CHECK** [Constraint 3]

## Examples

### Example 1
[Example 1]

### Example 2
[Example 2]
```
