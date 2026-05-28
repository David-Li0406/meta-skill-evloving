---
name: skill-manager
description: Use this skill when you need to manage the lifecycle of your skills, including checking for updates, listing skills, and enabling or disabling them.
---

# Skill Manager

This skill helps you manage the lifecycle of your skills by automating tasks such as checking for updates, listing skills, and performing health checks.

## Core Capabilities

1. **Audit**: Scans your local skills directory for skills with `source_url` metadata.
2. **Check**: Queries GitHub to compare local commit hashes against the latest remote HEAD.
3. **Report**: Generates a status report identifying which skills are "Stale" or "Current".
4. **Update Workflow**: Guides the agent through the process of upgrading a skill.
5. **Inventory Management**: Lists all local skills and provides deletion capabilities.
6. **Health Check**: Monitors skill health status, detecting outdated and invalid skills.
7. **Enable/Disable**: Temporarily enable or disable skills without deletion.

## Usage

**Existing Triggers**:
- `/skill-manager check` or "Scan my skills for updates"
- `/skill-manager list` or "List my skills"
- `/skill-manager delete <skill_name>` or "Delete skill <skill_name>"

**New Triggers**:
- `/skill-manager enable <skill_name>` or "Enable skill <skill_name>"
- `/skill-manager disable <skill_name>` or "Disable skill <skill_name>"
- `/skill-manager status` or "Check skill status"
- `/skill-manager health` or "Run health check"

### Workflow 1: Check for Updates

1. **Run Scanner**: The agent runs `scripts/scan_and_check.py` to analyze all skills.
2. **Review Report**: The script outputs a JSON summary. The agent presents this to the user.
    *   Example: "Found 3 outdated skills: `yt-dlp` (behind 50 commits), `ffmpeg-tool` (behind 2 commits)..."

### Workflow 2: Update a Skill

**Trigger**: "Update [Skill Name]" (after a check)

1. **Fetch New Context**: The agent fetches the *new* README from the remote repo.
2. **Diff Analysis**:
    *   The agent compares the new README with the old `SKILL.md`.
    *   Identifies new features, deprecated flags, or usage changes.
3. **Refactor**:
    *   The agent rewrites `SKILL.md` to reflect the new capabilities.
    *   The agent updates the `source_hash` in the frontmatter.
    *   The agent (optionally) attempts to update the `wrapper.py` if CLI args have changed.
4. **Verify**: Runs a quick validation to ensure the updates are correctly applied.

### Workflow 3: List Skills

1. **Run List Command**: The agent executes `scripts/list_skills.py` to retrieve all skills.
2. **Output**: Displays a formatted list of skills, including their names, types, versions, and descriptions.

### Workflow 4: Delete a Skill

1. **Run Delete Command**: The agent executes `scripts/delete_skill.py <skill_name>` to remove a skill.
2. **Confirmation**: The agent prompts the user for confirmation before proceeding with the deletion.

## Best Practices

1. **Regular Audits**: Regularly check for updates to ensure skills are current.
2. **Health Monitoring**: Use the health check feature to maintain skill integrity.
3. **Documentation**: Keep SKILL.md files updated with accurate descriptions and usage instructions.

## Example

### Example 1: Check for Updates

```
User: /skill-manager check
Agent: Scanning for updates...
Found 2 outdated skills: yt-dlp (behind 5 commits), ffmpeg-tool (up to date).
```