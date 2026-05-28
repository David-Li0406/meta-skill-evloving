---
name: managing-skills
description: Use this skill to install, update, list, and remove Claude skills from various sources, including GitHub repositories and .skill zip files.
---

# Managing Skills

This skill manages the lifecycle of Claude skills, allowing you to install, update, list, and remove skills from multiple source types, including GitHub repositories and .skill zip files.

## Purpose

This skill enables you to:
- **Install skills**: Add new skills from GitHub repositories, subdirectories, or .skill zip files.
- **Update skills**: Refresh existing skills to the latest version.
- **List installed skills**: View all currently installed skills and their details.
- **Remove skills**: Delete skills that are no longer needed.

## When to Use This Skill

Use this skill when you need to:
- Add new capabilities to Claude by installing skills from various sources.
- Check what skills are currently installed.
- Remove skills that are no longer needed.
- Manage skill dependencies and versions.

## Instructions

### Classifying Requests

Before any operation, classify what you want to do:

**Operation types:**
- INSTALL: Add a new skill
- UPDATE: Refresh an existing skill
- LIST: View installed skills
- REMOVE: Delete a skill
- CHECK: Verify skill source/status

**Source types for INSTALL/UPDATE:**
- GITHUB_REPO: `user/repo` or `github.com/user/repo`
- GITHUB_SUBDIR: URL contains `/tree/<branch>/` followed by a path
- SKILL_ZIP: URL ends with `.skill`

### Installing a Skill

To install a skill from a GitHub repository or a .skill file:

1. Identify the source type and provide the URL.
2. Choose the installation location:
   - **User skills** (`~/.claude/skills/`): Available across all projects.
   - **Project skills** (`<project>/.claude/skills/`): Available only in that project.

**Command for GitHub repo:**
```bash
mkdir -p ~/.claude/skills
git clone https://github.com/user/repo ~/.claude/skills/repo
```

**Command for .skill zip file:**
```bash
curl -L -o /tmp/skill.zip "https://example.com/skills/my-skill.skill"
mkdir -p ~/.claude/skills/my-skill
unzip -o /tmp/skill.zip -d ~/.claude/skills/my-skill
```

### Listing Installed Skills

To see all currently installed skills:
```bash
ls ~/.claude/skills/
```

### Removing a Skill

To remove an installed skill:
```bash
rm -rf ~/.claude/skills/skill-name
```

### Error Handling

Common errors and solutions:
- **Network failure**: Check internet connectivity and verify URL accessibility.
- **Permission denied**: Ensure you have write permissions on the target directory.
- **Skill already exists**: Ask the user for confirmation to overwrite or rename.

### Post-Installation

After installing any skill, check for and install dependencies if a `requirements.txt` file exists:
```bash
if [ -f ~/.claude/skills/skill-name/requirements.txt ]; then
  pip install -r ~/.claude/skills/skill-name/requirements.txt
fi
```

## Success Criteria

Installation is successful when:
- The skill directory exists at the target location.
- The SKILL.md file is present and readable.
- Dependencies are installed (if applicable).
- User is reminded to restart Claude Code.

Update is successful when:
- The latest version is pulled/downloaded.
- No merge conflicts occur.

Removal is successful when:
- The skill directory no longer exists.

## Examples

### Example 1: Installing a Skill from GitHub
```bash
git clone https://github.com/user/repo ~/.claude/skills/repo
```

### Example 2: Listing Installed Skills
```bash
ls ~/.claude/skills/
```

### Example 3: Removing a Skill
```bash
rm -rf ~/.claude/skills/skill-name
```

## References

For more information, see:
- [GitHub API Documentation](https://docs.github.com/en/rest)