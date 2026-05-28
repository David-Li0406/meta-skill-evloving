---
name: create-update-agent-skill
description: Use this skill when you need to create a new agent skill or update an existing one following the agent skill specification.
---

# Create/Update Agent Skill

**`GOAL`**: Create or update an agent skill directory, standard sub-folders, and a compliant `SKILL.md` template based on the agent skills specification.

## When to Use This Skill

- When the user asks to create a new skill.
- When the user asks to update an existing skill.
- When the user wants to add functionality as a reusable skill.
- When the user wants to modify skill documentation or behavior.

## Prerequisites

- The `skills/` directory must exist.
- The requested skill name must be in kebab-case (lowercase, alphanumeric, dashes) and must not start or end with a hyphen or contain consecutive hyphens.
- `references/skill-reference-guide.md` must exist.

## Workflow

### Step 1: Check Input

- Verify the skill name follows kebab-case conventions.
- Check if `skills/<name>` already exists.
- If it exists: emit `ERROR: Skill <name> already exists`.

### Step 2: Create Directory Structure

- For new skills, create the directory: `skills/<name>/`.
- Create standard subdirectories: `scripts/`, `references/`, `assets/`, `tests/`.
- For existing skills, locate the existing skill directory and read the existing `SKILL.md` to understand the current structure.

### Step 3: Generate `SKILL.md`

The `SKILL.md` file must contain:

#### Required Frontmatter

```yaml
---
name: <skill-name>
description: <text description of what the skill does and when to use it>
---
```

**Critical Rules:**

- `name` in frontmatter must match the directory name.
- `description` should clearly explain what the skill does and when to use it (1-1024 characters).

#### Required Sections

1. **Skill Title and Introduction**
   ```markdown
   # AI Builder - {Skill Name}
   Brief introduction describing what this skill does.
   ```

2. **When to Use This Skill**
   ```markdown
   ## When to Use This Skill
   - Bullet point describing use case 1
   - Bullet point describing use case 2
   ```

3. **Your Roles in This Skill**
   ```markdown
   ## Your Roles in This Skill
   - **Project Manager**: Coordinate the skill creation/update process.
   - **Backend Developer**: Implement the skill structure and write clear instructions.
   - **Technical Writer**: Document the skill clearly with examples and usage guidelines.
   ```

4. **Role Communication**
   ```markdown
   ## Role Communication
   As an expert in your assigned roles, you must announce your actions before performing them using the following format:
   As a {Role}, I will {action description}.
   ```

5. **Instructions**
   ```markdown
   ## Instructions
   Follow these steps in order:
   ### Step 1: {Step Title}
   Detailed instructions for this step...
   ```

### Step 4: Create Reference Files (If Needed)

- Use reference files to keep `SKILL.md` concise. Create separate files for different tools, platforms, or installation methods.
- Link to them from `SKILL.md` using relative paths.

### Step 5: Add Scripts (If Needed)

If your skill includes executable scripts:

1. Create the `scripts/` directory.
2. Add scripts that are self-contained and include helpful error messages.

### Step 6: Validate the Skill

Check the following:

1. Frontmatter validation: Ensure `name` matches the directory name and is in the correct format.
2. Required sections are present.
3. Instructions are clear and step-by-step.

### Step 7: Test the Skill (Optional)

If possible, test the skill by walking through the instructions manually and verifying all file references work.

### Step 8: Ask for User Confirmation

Show the user the skill name, location, summary of what the skill does, and any additional notes or recommendations. Ask for confirmation to proceed.

## Key Principles

- Follow the agent skills specification.
- Keep `SKILL.md` concise and defer detailed content to reference files.
- Ensure clear instructions and appropriate role assignments.

## Common Issues

- Ensure the skill name matches the directory.
- Avoid including steps to update documentation files unless explicitly requested.
- Always create separate reference files for different tools or platforms.