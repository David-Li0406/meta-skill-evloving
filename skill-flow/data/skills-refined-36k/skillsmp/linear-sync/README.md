# linear-sync

Updates Linear issues based on implementation evidence from `/project-status`.

## Overview

This skill bridges the gap between code reality and issue tracking. It reads evidence from local repositories, GitHub, and transcripts (via `/project-status`), then updates Linear issues to reflect actual development progress.

## Usage

```
/linear-sync [components...]
```

### Examples

```bash
# Sync all components
/linear-sync

# Sync specific components
/linear-sync auth dashboard

# After running project-status
"Update Linear based on that status"
```

## How It Works

1. **Gathers evidence** by invoking `/project-status`
2. **Queries Linear** for current issue states
3. **Matches components** to Linear issues by title
4. **Shows preview** of proposed changes
5. **Requests confirmation** before any updates
6. **Applies updates** and adds explanatory comments

## Status Mapping

| Evidence Status | Linear State |
|----------------|--------------|
| Shipped | Done |
| Done | Done |
| In Review | In Review |
| In Progress | In Progress |
| Todo | Todo |
| Backlog | Backlog |
| Triage | Triage |

**Key rule:** Only upgrades status. Never downgrades automatically.

## Configuration

Requires Linear settings in `.entourage/repos.json`:

```json
{
  "linear": {
    "teamId": "TEAM",
    "workspace": "my-workspace"
  }
}
```

## Safety Features

- **Preview before changes** - Always shows what will be updated
- **Confirmation required** - No silent modifications
- **Upgrade-only** - Never downgrades status
- **Comment trail** - Adds evidence comments to updated issues
- **No auto-create** - Prompts before creating new issues

## Output Format

### Preview
```
| Component | Issue | Current | Proposed | Evidence |
|-----------|-------|---------|----------|----------|
| auth | TEAM-123 | Backlog | In Progress | Feature branch |
```

### Results
```
## Updated (1)
| Issue | Previous | New | Evidence |
|-------|----------|-----|----------|
| TEAM-123 | Backlog | In Progress | Feature branch exists |
```

## Related Skills

- `/project-status` - Gathers implementation evidence (read-only)
- `/linear-check` - Queries Linear issue status (read-only)
- `/local-repo-check` - Scans local git repositories
- `/github-repo-check` - Queries GitHub API
