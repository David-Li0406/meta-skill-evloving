---
name: new-agent-skill
description:
  Creates a new agent skill. Use when agent or user needs to create a
  new skill for the agent.
---

# New agent skill

**`GOAL`**: create a new skill directory, standard sub-folders, and a
compliant `SKILL.md` template based on the local reference guide.

**`WHEN`**: you need to create a new skill for the agent.

## Prerequisites

- The `skills/` directory must exist.
- The requested skill name requires kebab-case (lowercase, alphanumeric,
  dashes).
- `references/skill-reference-guide.md` must exist.

## Efficiency directives

- Create all directories and files in a single pass.
- Optimize all operations for agent, token, and context efficiency.

## Workflow

### Step 1: Check input

- Verify the skill name follows kebab-case conventions.
- Check if `skills/<name>` already exists.
- If exists: emit `ERROR: Skill <name> already exists`.

### Step 2: Create directory structure

- Create `skills/<name>/`.
- Create `skills/<name>/SKILL.md`.
- Create standard subdirectories: `scripts/`, `references/`, `assets/`,
  `tests/`.

### Step 3: Generate `SKILL.md`

- Refine, streamline and optimize the user's instructions for the new
  skill.
- Read `references/skill-reference-guide.md`.
- Update `SKILL.md` using the reference and user's instructions. Output.

### Step 4: Report completion

- Output `SUCCESS: Created skill <name> at skills/<name>/`.

## References

- `references/skill-reference-guide.md`: The authoritative guide for
  skill structure and templating.
