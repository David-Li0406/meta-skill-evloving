---
name: skill-updating
description: Update existing skills in ~/dotfiles/skills. Use when the user asks to modify, update, or improve a skill's description or functionality.
---

# Skill Updating

Update existing skills stored in `~/dotfiles/skills`.

## Usage

Skills are located in: `~/dotfiles/skills/`

Each skill is a directory containing:
- `SKILL.md` - The main skill file with frontmatter and documentation
- `scripts/` - Optional directory for executable scripts

## Skill Structure

The `SKILL.md` file has:

1. **Frontmatter** (between `---` markers):
   - `name`: The skill name (must match directory name)
   - `description`: Short description shown in skill tool listing. Should clearly indicate when to use the skill.

2. **Markdown Content**: Documentation about what the skill does and how to use it

## Updating a Skill

To update a skill:

1. Read the existing skill file: `~/dotfiles/skills/<skill-name>/SKILL.md`
2. Use the Edit tool to modify the frontmatter description or content
3. Ensure the description clearly indicates when Claude should use the skill

## Example Frontmatter

```yaml
---
name: example-skill
description: Do X when user asks for Y. Use when the user wants to Z.
---
```

## Available Skills

Check what skills exist:

```bash
ls ~/dotfiles/skills/
```
