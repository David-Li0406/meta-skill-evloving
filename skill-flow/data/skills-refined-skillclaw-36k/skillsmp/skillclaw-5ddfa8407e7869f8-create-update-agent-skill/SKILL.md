---
name: create-update-agent-skill
description: Use this skill when you need to create a new agent skill or update an existing one to ensure compliance with the Agent Skills specification.
---

# Create/Update Agent Skill

**`GOAL`**: Create a new agent skill directory, standard sub-folders, and a compliant `SKILL.md` template, or update an existing skill to match the standard.

## When to Use This Skill

- When the user asks to create a new skill.
- When the user requests to update an existing skill.
- When the user wants to add functionality as a reusable skill.
- When the user wants to modify skill documentation or behavior.

## Prerequisites

1. **Identify the Skill Name**:
   - Must be 1-64 characters.
   - Only lowercase alphanumeric (a-z, 0-9) and hyphens (-).
   - Cannot start or end with a hyphen.
   - Cannot have consecutive hyphens (`--`).

2. **Understand the Purpose**: Clarify what task the skill is solving to write a good description.

## Workflow

### Step 1: Check Input

- Verify the skill name follows kebab-case conventions.
- Check if `skills/<name>` already exists.
- If it exists: emit `ERROR: Skill <name> already exists`.

### Step 2: Create or Locate the Skill Directory

**For new skills:**

1. Create the skill directory: `skills/<name>/`.
2. Create standard subdirectories: `scripts/`, `references/`, `assets/`.

**For existing skills:**

1. Locate the existing skill directory: `skills/<name>/`.
2. Read the existing `SKILL.md` to understand the current structure.

### Step 3: Create/Update `SKILL.md`

The `SKILL.md` file must contain:

#### Required Frontmatter

```yaml
---
name: <skill-name>
description: <text description of what the skill does and when to use it>
---
```

**Critical Rules:**

- `name` in frontmatter MUST match the directory name.
- `description` should include keywords to help agents find the skill (1-1024 chars).

### Step 4: Populate Optional Directories (If needed)

- **scripts/**: For code that needs to be executed (e.g., Python scripts). Ensure they are self-contained.
- **references/**: For static knowledge, cheat sheets, or lookup tables.
- **assets/**: For templates the agent should copy or use.

### Step 5: Report Completion

- Output `SUCCESS: Created skill <name> at skills/<name>/` or `SUCCESS: Updated skill <name> at skills/<name>/`.

## Validation

After creating or updating the files, ensure:

1. The directory name and `name` field match exactly.
2. The YAML frontmatter is valid.
3. All required sections are included and adhere to specifications.