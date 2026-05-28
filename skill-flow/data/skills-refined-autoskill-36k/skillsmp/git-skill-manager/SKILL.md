---
name: git-skill-manager
description: Install, manage, and remove Claude skills from GitHub repositories. Use
  when you need to add new skills from git or manage installed skills.
license: MIT
metadata:
  author: agent-starter
  version: 2.0.0
  keywords:
  - git
  - github
  - skill
  - installation
  - management
  - plugin
allowed-tools: Bash(python:*) Read Write
tags: 30_Resources
---
# Git Skill Manager

A skill for installing, managing, and removing Claude skills directly from GitHub repositories. This skill automates the process of downloading skill packages from git and integrating them into your `.claude/skills` directory.

## Purpose

This skill enables you to:
- **Install skills from GitHub**: Automatically download and install skill packages from any public GitHub repository
- **Track installations**: Maintain a registry of all installed skills with metadata
- **Manage skills**: List all installed skills with their details
- **Remove skills**: Clean up skills you no longer need

## When to Use This Skill

Use this skill when you need to:
- Add new capabilities to Claude by installing skills from GitHub
- Check what skills are currently installed
- Remove skills that are no longer needed
- Manage skill dependencies and versions

## Instructions

### Installing a Skill from GitHub

To install a skill from a GitHub repository:

1. Identify the GitHub repository URL containing the skill (must be a public repository)
2. Run the install command with the repository URL
3. The skill will automatically:
   - Download all skill files from the repository
   - Extract skills from the `.claude/skills/` directory
   - Install them to your local `.claude/skills/` folder
   - Register the installation in the registry

**Command:**
```bash
python .claude/skills/git-skill-manager/scripts/manage.py install --git-url "REPOSITORY_URL"
```

**Optional parameters:**
- `--plugin-name`: Custom name for the plugin (default: repository name)
- `--target-path`: Installation directory (default: `.claude`)

### Listing Installed Skills

To see all currently installed skills:

```bash
python .claude/skills/git-skill-manager/scripts/manage.py list
```

This displays:
- Plugin name
- Repository URL
- Owner
- Installation timestamp
- List of skills included in the plugin

### Removing a Skill

To remove an installed skill:

1. First, list installed skills to find the exact skill name
2. Run the uninstall command with the skill name

```bash
python .claude/skills/git-skill-manager/scripts/manage.py uninstall --skill-name "SKILL_NAME"
```

This will:
- Delete the skill directory and all its files
- Remove the entry from the registry
- Report the number of files deleted

## Examples

### Example 1: Installing Obsidian Skills

```bash
python scripts/manage.py install --git-url "https://github.com/kepano/obsidian-skills"
```

**Output:**
```
📦 'obsidian-skills' 다운로드 중...
✓ 플러그인 'obsidian-skills'이(가) 성공적으로 설치되었습니다.
✓ 3개의 skill이 설치되었습니다:
  - .claude/skills/json-canvas
  - .claude/skills/obsidian-bases
  - .claude/skills/obsidian-markdown
```

### Example 2: Listing Installed Skills

```bash
python scripts/manage.py list
```

**Output:**
```
📋 설치된 Plugin 목록 (1개):
============================================================
1. obsidian-skills
   Repository: https://github.com/kepano/obsidian-skills
   Owner: kepano
   Installed: 2026-01-23T21:00:00
   Skills: json-canvas, obsidian-bases, obsidian-markdown
============================================================
```

### Example 3: Removing a Skill

```bash
python scripts/manage.py uninstall --skill-name "json-canvas"
```

**Output:**
```
🗑️  'json-canvas' 제거 중...
✓ 스킬 'json-canvas'이(가) 성공적으로 제거되었습니다.
✓ 5개의 파일이 삭제되었습니다.
```

## Registry Management

Installed skills are tracked in `assets/registry.json`:

```json
{
  "version": "1.0.0",
  "plugins": [
    {
      "name": "obsidian-skills",
      "git_url": "https://github.com/kepano/obsidian-skills",
      "owner": "kepano",
      "repo": "obsidian-skills",
      "target_path": ".claude",
      "installed_at": "2026-01-23T21:00:00.000000",
      "skills": ["obsidian-markdown", "obsidian-bases", "json-canvas"],
      "status": "installed"
    }
  ],
  "last_updated": "2026-01-23T21:00:00.000000"
}
```

## Error Handling

Common errors and solutions:

**"Invalid Git URL"**
- Ensure the URL is in the format: `https://github.com/owner/repo`
- Verify the repository exists and is public

**"Skill not found"**
- Use the `list` command to see exact skill names
- Skill names are case-sensitive

**"HTTP Error"**
- Check your internet connection
- Verify the repository is accessible
- Ensure the repository has a `.claude/skills/` directory

**"Permission denied"**
- Ensure you have write permissions to the `.claude/skills` directory
- Check file system permissions

## Requirements

- Python 3.6 or higher
- Internet connection for GitHub API access
- Write permissions to `.claude/skills` directory

## File Structure

```
git-skill-manager/
├── SKILL.md              # This file
├── README.md             # Quick start guide
├── scripts/              # Executable scripts
│   ├── manage.py        # Main CLI script
│   ├── example.py       # Usage examples
│   └── validate.py      # Validation script
├── assets/               # Data and templates
│   └── registry.json    # Installation registry
└── references/           # Reference documentation
    ├── QUICKREF.md      # Quick reference card
    ├── MIGRATION.md     # Migration guide
    └── COMPLETION.md    # Completion report
```

## References

For more information, see:
- [Quick Reference](references/QUICKREF.md) - Command cheat sheet
- [Migration Guide](references/MIGRATION.md) - Changes from previous version
- [Agent Skills Specification](https://agentskills.io/specification)
- [GitHub API Documentation](https://docs.github.com/en/rest)
