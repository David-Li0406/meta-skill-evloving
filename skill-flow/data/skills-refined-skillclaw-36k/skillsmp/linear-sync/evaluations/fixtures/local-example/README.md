# Local Testing Fixture Template

## Setup

1. Copy this directory: `cp -r local-example local-myteam`
2. Edit `.entourage/repos.json` with your Linear team configuration
3. Your directory is gitignored (`local-*` pattern)

## Warning: Write Operation Tests

When running with `LINEAR_SYNC_AUTO_CONFIRM=1`, the test harness will:

- **CREATE** temporary issues prefixed with `[TEST]`
- **MODIFY** issue status, assignee, and due date
- **CANCEL** test issues after completion (auto-archives later)

### Recommendation

Consider creating a **dedicated test workspace** in Linear if you're
concerned about test data appearing in your production workspace.

All test issues are:
- Clearly marked with `[TEST]` prefix
- Designed to be temporary and auto-cleaned
- Safe to delete manually if needed

## Configuration

Edit `.entourage/repos.json` with your workspace details:

```json
{
  "linear": {
    "teamId": "YOUR_TEAM_KEY",
    "workspace": "your-workspace-slug"
  },
  "repos": [
    {
      "name": "your-repo",
      "path": ".",
      "github": "your-org/your-repo"
    }
  ]
}
```

### Finding Your Team Key

1. Open Linear and navigate to your team
2. Look at the URL: `https://linear.app/your-workspace/team/TEAM-KEY/...`
3. The team key is typically 2-4 uppercase letters (e.g., "ENT", "TEAM")

### Finding Your Workspace Slug

1. Look at your Linear URL: `https://linear.app/your-workspace-slug/...`
2. Use the slug portion after `linear.app/`

## Run Tests

```bash
# Run all linear-sync tests (auto-confirm enabled by harness)
./tests/run.sh linear-sync

# Dry run to see what would execute
./tests/run.sh --dry-run linear-sync

# Verbose output
./tests/run.sh --verbose linear-sync
```

## Cleanup

If test issues remain in your workspace:

1. Search Linear for issues with `[TEST]` in the title
2. Bulk select and set status to Canceled
3. Linear will auto-archive canceled issues based on your workspace settings
