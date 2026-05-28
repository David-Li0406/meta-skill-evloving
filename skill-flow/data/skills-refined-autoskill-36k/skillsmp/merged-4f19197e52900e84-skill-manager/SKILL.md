---
name: skill-manager
description: Use this skill to manage the lifecycle of skills, including scanning for updates, checking GitHub repositories, upgrading, and inventory management.
---

# Skill Manager

This skill helps you maintain your library of skills by automating the detection of updates and assisting in the management process.

## Core Capabilities

1. **Audit**: Scans your skills directory for skills with `source_url` or `github_url` metadata.
2. **Check**: Queries GitHub (via `git ls-remote`) to compare local commit hashes against the latest remote HEAD.
3. **Report**: Generates a status report identifying which skills are "Stale", "Current", "Unmanaged", or "Error".
4. **Update Workflow**: Provides a structured process for the agent to upgrade a skill.
5. **Inventory Management**: Lists all local skills and provides deletion capabilities.
6. **Health Check**: Monitors skill health status, detecting outdated and invalid skills.
7. **Enable/Disable**: Temporarily enable or disable skills without deletion.

## Usage

### Check for Updates

**Triggers**:
- `/skill-manager check`
- "Scan my skills for updates"

**Workflow**:
1. The agent runs `scripts/scan_and_check.py <skills_dir>`.
2. The script concurrently checks all skills with `source_url` or `github_url`.
3. Outputs a JSON status report.
4. The agent presents the results to the user.

### List Skills

**Triggers**:
- `/skill-manager list`
- "List my skills"

**Workflow**:
1. The agent runs `scripts/list_skills.py <skills_dir>`.
2. Outputs a table or JSON format of the skills list.

### Update a Skill

**Trigger**: "Update [Skill Name]" (after a check)

**Workflow**:
1. The agent fetches the new README from the remote repository.
2. Compares the new README with the old `SKILL.md` to identify changes.
3. Updates `SKILL.md` to reflect new capabilities and updates the `source_hash` or `github_hash`.
4. Optionally updates the `wrapper.py` if CLI args have changed.

### Delete a Skill

**Triggers**:
- `/skill-manager delete <skill_name>`
- "Delete skill <skill_name>"

**Workflow**:
1. The agent runs `scripts/delete_skill.py <skill_name> <skills_dir>`.
2. The script displays skill information and requests confirmation.
3. Optionally backs up to a `.skill-backup` directory before deletion.

### Enable/Disable a Skill

**Triggers**:
- `/skill-manager enable <skill_name>`
- `/skill-manager disable <skill_name>`

**Workflow**:
1. **Disable**: Moves the skill directory to a `.disabled/` subdirectory.
2. **Enable**: Moves the skill directory back to the main directory.

### Health Check

**Triggers**:
- `/skill-manager health`
- "Run health check"

**Workflow**:
1. The agent runs `scripts/health_check.py <skills_dir>`.
2. Outputs a summary showing healthy, outdated, and invalid skills.
3. Based on the report, the user can update or clean up problematic skills.

## Metadata Requirements

This manager relies on the following metadata fields:
- `source_url` or `github_url`: Source of truth.
- `source_hash` or `github_hash`: State of truth.
- `version`: Semantic versioning.

## Best Practices

1. **Regular Checks**: It is recommended to run `/skill-manager check` weekly.
2. **Backup Before Deletion**: Use the `--backup` option before deleting important skills.
3. **Post-Update Alignment**: After updating a skill, run the relevant alignment scripts to restore user experience.

## Collaboration with Other Skills

- **skill-factory**: Skills created automatically include necessary metadata for lifecycle management.
- **skill-evolution**: Calls alignment scripts after updates to restore user experience.
- **skill-creator**: Follows the same metadata standards for compatibility.