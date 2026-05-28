---
name: skill-creator
description: Use this skill to create new skills for the workspace.
metadata:
  source: https://github.com/anthropics/skills/tree/main/skills/skill-creator
---

# Skill Creator Skill

Use this skill when asked to "create a new skill", "make a skill for X", or "scaffold a skill".

## Skill Creation Process

Skill creation involves these steps:

1.  **Understand the skill**: What is the goal? What tools/scripts does it need?
2.  **Initialize**: Run the initialization script to scaffold the directory.
3.  **Edit**: Populate `SKILL.md` and add scripts/references.
4.  **Validate**: Check the structure.

## Usage

### 1. Initialize a New Skill
Run the initialization script from the workspace root:

```bash
python3 .agent/skills/skill-creator/scripts/init_skill.py <skill-name>
```

-   `<skill-name>`: Hyphen-case name (e.g., `git-helper`, `data-processing`).
-   By default, this creates the skill in `.agent/skills/<skill-name>`.
-   Use `--path <path>` to specify a different parent directory if needed.

### 2. Customize the Skill
The initialization script creates:
-   `SKILL.md`: The main instruction file. **You must edit this** to describe what the skill does.
-   `scripts/`: Directory for executable tools (Python/Bash).
-   `references/`: Directory for documentation context.
-   `assets/`: Directory for file templates/assets.

### 3. Validate
Run the validation script to ensure the skill follows conventions:

```bash
python3 .agent/skills/skill-creator/scripts/quick_validate.py .agent/skills/<skill-name>
```
