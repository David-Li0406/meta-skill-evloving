---
name: create-update-agent-skill
description: Use this skill when you need to create a new agent skill or update an existing one following the agent skill specification.
---

# Create/Update Agent Skill

**`GOAL`**: Create a new skill directory, standard sub-folders, and a compliant `SKILL.md` template based on the agent skills specification.

## When to Use This Skill

- When the user asks to create a new skill.
- When the user asks to update an existing skill.
- When the user wants to add functionality as a reusable skill.
- When the user wants to modify skill documentation or behavior.

## Prerequisites

- The `skills/` directory must exist.
- The requested skill name must be in kebab-case (lowercase, alphanumeric, dashes) and must not start or end with a hyphen or contain consecutive hyphens.
- The `references/skill-reference-guide.md` must exist.

## Workflow

### Step 1: Check Input

- Verify the skill name follows kebab-case conventions.
- Check if `skills/<name>` already exists.
- If it exists: emit `ERROR: Skill <name> already exists`.

### Step 2: Create Directory Structure

- Create `skills/<name>/`.
- Create `skills/<name>/SKILL.md`.
- Create standard subdirectories: `scripts/`, `references/`, `assets/`.

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

#### Body Structure

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

   As a {Role}, I will {action description}
   ```

5. **Instructions**
   ```markdown
   ## Instructions

   Follow these steps in order:

   ### Step 1: {Step Title}

   Detailed instructions for this step...

   ### Step 2: {Step Title}

   Detailed instructions for this step...
   ```

### Step 4: Validate the Skill

**Check the following:**

1. **Frontmatter validation:**
   - `name` matches directory name.
   - `description` is clear and under 1024 characters.

2. **Required sections present:**
   - Skill title and introduction.
   - "When to Use This Skill".
   - "Your Roles in This Skill".
   - "Role Communication".
   - "Instructions".

3. **Content quality:**
   - Instructions are clear and step-by-step.
   - Roles are appropriate for the task.

### Step 5: Create Reference Files (IMPORTANT)

**Always use reference files to keep `SKILL.md` concise.** Prefer routing details to `references/` files rather than embedding everything in `SKILL.md`.

### Step 6: Add Scripts (if needed)

If your skill includes executable scripts:

1. **Create `scripts/` directory**.
2. **Add scripts** that are self-contained and include helpful error messages.

### Step 7: Test the Skill (Optional)

If possible, test the skill by:
1. Walking through the instructions manually.
2. Verifying all file references work.

### Step 8: Ask for User Confirmation

Show the user:
1. The skill name and location.
2. Summary of what the skill does.
3. List of files created/updated.
4. Any additional notes or recommendations.

## Key Principles

- Follow the specification and keep `SKILL.md` concise.
- Use reference files proactively for different tools, platforms, and methods.
- Clear instructions are essential for usability.

## Common Issues

- Ensure the `name` in frontmatter matches the directory name.
- All skills must follow the naming conventions and structure outlined above.