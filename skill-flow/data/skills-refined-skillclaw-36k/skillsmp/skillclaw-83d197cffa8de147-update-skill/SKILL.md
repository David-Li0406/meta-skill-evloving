---
name: update-skill
description: Use this skill to update a skill from the canonical ClaudeSkills repository, ensuring your local skills are synchronized with the latest versions.
---

# update-skill

Updates a skill in the current project from the canonical [stoicstudio/ClaudeSkills](https://github.com/stoicstudio/ClaudeSkills) repository.

> **Canonical Source**: This skill is maintained at [stoicstudio/ClaudeSkills](https://github.com/stoicstudio/ClaudeSkills).

## Arguments

- `skill_name` (required): Name of the skill to update (e.g., `publish-release`).

## Steps

1. **Parse the skill name** from the command arguments.

2. **Check if the skill exists locally**:
   ```bash
   ls .claude/skills/{skill_name}/SKILL.md
   ```
   - If not found, this will be a fresh install.

3. **Get the current local version** (if it exists):
   ```bash
   head -10 .claude/skills/{skill_name}/SKILL.md | grep "^version:"
   ```

4. **Fetch canonical version info**:
   ```bash
   curl -sL "https://raw.githubusercontent.com/stoicstudio/ClaudeSkills/main/skills/{skill_name}/SKILL.md" | head -10
   ```
   - If 404, report that the skill doesn't exist in the canonical repo.
   - Extract the version from frontmatter.

5. **Compare versions**:
   - If the same version: Report "Already up to date (v{version})".
   - If different or new install: Proceed with the update.

6. **Create the skill directory** if needed:
   ```bash
   mkdir -p .claude/skills/{skill_name}
   ```

7. **Download and install the skill**:
   ```bash
   curl -sL "https://raw.githubusercontent.com/stoicstudio/ClaudeSkills/main/skills/{skill_name}/SKILL.md" \
     -o .claude/skills/{skill_name}/SKILL.md
   ```

8. **Verify installation**:
   ```bash
   head -10 .claude/skills/{skill_name}/SKILL.md
   ```

9. **Report result**:
   - New install: "Installed {skill_name} v{version}".
   - Update: "Updated {skill_name}: v{old} → v{new}".
   - Remind the user to commit the change if desired.

## Available Skills

Skills available in the canonical repository:

| Skill | Description |
|-------|-------------|
| `publish-release` | Publish releases to GitHub Packages. |
| `update-skill` | Update skills from the canonical repo (this skill). |

To see all available skills:
```bash
curl -sL "https://api.github.com/repos/stoicstudio/ClaudeSkills/contents/skills" | jq -r '.[].name'
```

## Examples

```
/update-skill publish-release    # Update the publish-release skill
```