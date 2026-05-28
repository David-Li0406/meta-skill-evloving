---
name: skill-management
description: Use this skill when you need to install, update, list, or remove Claude skills from various sources, including GitHub repositories and zip files.
---

# Skill body

## Purpose

This skill enables you to manage Claude skills throughout their lifecycle, including installation, updates, listing, and removal.

## When to Use This Skill

Use this skill when you need to:
- Add new capabilities to Claude by installing skills from GitHub or zip files.
- Update existing skills to their latest versions.
- List all currently installed skills and their details.
- Remove skills that are no longer needed.

## Instructions

### Classifying Your Request

Before performing any operation, classify what you want to do:

**Operation types:**
- **INSTALL**: Add a new skill.
- **UPDATE**: Refresh an existing skill.
- **LIST**: View installed skills.
- **REMOVE**: Delete a skill.
- **CHECK**: Verify skill source/status.

**Source types (for INSTALL/UPDATE):**
- **GITHUB_REPO**: `user/repo` or `github.com/user/repo`.
- **GITHUB_SUBDIR**: URL contains `/tree/<branch>/` followed by a path.
- **SKILL_ZIP**: URL ends with `.skill`.

### Installing a Skill

To install a skill from a GitHub repository or a zip file:

1. Identify the source type and provide the appropriate URL.
2. Choose the installation location:
   - **User skills**: `~/.claude/skills/<skill-name>/` (available in all projects).
   - **Project skills**: `<project>/.claude/skills/<skill-name>/` (available only in that project).
3. Run the install command:

```bash
python .claude/skills/skill-management/scripts/manage.py install --source "SOURCE_URL" --location "LOCATION"
```

### Updating a Skill

To update an existing skill:

1. Identify the skill name and source.
2. Run the update command:

```bash
python .claude/skills/skill-management/scripts/manage.py update --skill-name "SKILL_NAME"
```

### Listing Installed Skills

To see all currently installed skills:

```bash
python .claude/skills/skill-management/scripts/manage.py list
```

This displays:
- Skill name
- Source URL
- Installation timestamp

### Removing a Skill

To remove an installed skill:

1. List installed skills to find the exact skill name.
2. Run the uninstall command with the skill name:

```bash
python .claude/skills/skill-management/scripts/manage.py remove --skill-name "SKILL_NAME"
```

### Verifying Installation

After installation or update, confirm that the skill is correctly installed:

- Check that the SKILL.md exists in the target location.
- Install dependencies if a `requirements.txt` exists.
- Report success to the user.