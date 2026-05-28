---
name: update-issue
description: "Update external issue tracker (GitHub/GitLab) based on Ralf events. Use when syncing story status with project management tools."
---

# Update Issue Skill

Expert guidance for updating issue status in external trackers based on Ralf events.

## When to Use

- Syncing story status with GitHub Issues
- Updating GitLab issues during Ralf execution
- Automating issue tracker updates via hooks
- Manual status updates via command

## Supported Platforms

### GitHub (via gh CLI or MCP)

```bash
# Add label
gh issue edit <issue_number> --add-label "in-progress"

# Remove label
gh issue edit <issue_number> --remove-label "in-progress"

# Add comment
gh issue comment <issue_number> --body "Starting implementation..."

# Close issue
gh issue close <issue_number> --comment "Completed!"
```

### GitLab (via MCP GitLab Server)

Use the MCP GitLab tools when available:
- `mcp__noqta_gitlab_server__update_issue` - Update issue attributes
- `mcp__noqta_gitlab_server__create_issue_note` - Add comments

Or via glab CLI:
```bash
# Update labels
glab issue update <issue_number> --label "in-progress"

# Add comment
glab issue note <issue_number> --message "Starting implementation..."

# Close issue
glab issue close <issue_number>
```

## Story ID Formats

The skill auto-detects issue format from story ID:

| Format | Platform | Example |
|--------|----------|---------|
| `#123` | GitHub/GitLab | `#42` |
| `PROJ-123` | Jira | `AUTH-101` |
| `US-001` | Custom (needs mapping) | Map in prd.json |

## Issue Mapping

For custom story IDs, add mapping to prd.json:

```json
{
  "userStories": [
    {
      "id": "US-001",
      "title": "Add login",
      "issueRef": {
        "platform": "github",
        "number": 42
      }
    }
  ]
}
```

## Status Mapping

| Ralf Event | GitHub Action | GitLab Action |
|------------|---------------|---------------|
| `on_task_start` | Add "in-progress" label | Add "in-progress" label |
| `on_task_completed` | Remove "in-progress", optionally close | Remove "in-progress" |
| `on_task_blocked` | Add "blocked" label, comment | Add "blocked" label, comment |

## Platform Detection

Auto-detect platform from git remote:

```bash
# Get remote URL
REMOTE=$(git remote get-url origin)

# Check platform
if [[ "$REMOTE" == *"github.com"* ]]; then
  PLATFORM="github"
elif [[ "$REMOTE" == *"gitlab"* ]]; then
  PLATFORM="gitlab"
fi
```

## Hook Integration

The update-issue skill is typically invoked via lifecycle hooks:

```bash
# In .ralf/hooks/on-task-start.sh
STORY_ID=$(echo "$CONTEXT" | jq -r '.storyId')

if [[ "$STORY_ID" =~ ^#([0-9]+)$ ]]; then
  ISSUE_NUM="${BASH_REMATCH[1]}"
  gh issue edit "$ISSUE_NUM" --add-label "in-progress"
fi
```

## Configuration

Project-level configuration in `.ralf/config.json`:

```json
{
  "settings": {
    "issueTracker": {
      "platform": "github",
      "autoUpdate": true,
      "labelOnStart": "in-progress",
      "labelOnComplete": null,
      "labelOnBlocked": "blocked",
      "closeOnComplete": false
    }
  }
}
```

## Error Handling

- If issue doesn't exist: Log warning, continue
- If label doesn't exist: Create it or skip
- If API rate limited: Retry with backoff
- If auth fails: Log error, don't block execution

## Best Practices

1. **Use optional hooks**: Don't block Ralf execution on issue tracker failures
2. **Keep comments concise**: Include key metrics, not full logs
3. **Use consistent labels**: Define label set in project config
4. **Handle missing issues**: Story may not have corresponding issue

## Example Comment Templates

### On Start
```
Starting implementation on branch `ralf/feature-name` (iteration 1)
```

### On Complete
```
Completed in 5m 30s using 25,000 tokens.

Commit: `abc123def`
Files changed: src/auth.ts, src/login.tsx
```

### On Blocked
```
Blocked after 3 attempts.

**Reason:** Typecheck failed - missing dependency

**Errors:**
- Cannot find module 'auth-lib'
- Type 'User' is not assignable to type 'AuthUser'

Manual intervention required.
```
