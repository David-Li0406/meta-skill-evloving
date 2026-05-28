---
name: managing-github-issues
description: Use this skill for comprehensive management of GitHub issues, including listing, creating, updating, and fixing issues with worktree isolation.
---

# Managing GitHub Issues Skill

Manage GitHub issues from listing to fixing to PR creation with clean worktree isolation.

## Commands

- `/managing-github-issues` - Main entry point for all issue operations

## Agents

- `issue-intake-agent` - List and fetch issue details
- `issue-mutate-agent` - Create and update issues
- `issue-fix-agent` - Implement fixes in isolated worktrees
- `issue-pr-agent` - Create pull requests

## Operations

- `--list [--repo owner/repo]` - List open issues
- `--create` - Create issue interactively
- `--update <id>` - Update issue fields
- `--fix --issue <id/url> [--yolo]` - Full fix workflow: fetch → confirm → worktree → implement → test → commit → push → PR

## Dependencies

- **Skills**: sc-git-worktree (worktree operations)
- **CLI**: GitHub CLI (`gh`) required
- **Config**: Configuration options can be set in `.claude/config.yaml` or via package manifest.

## Configuration

Default configuration options:

```yaml
base_branch: main
branch_pattern: "fix-issue-{number}"
auto_pr: true
```

Users can override in `.claude/config.yaml`:

```yaml
github:
  base_branch: develop
  branch_pattern: "hotfix/{number}"
  auto_pr: false
  test_command: "npm test"
  pr_template: |
    ## Summary
    Fixes #{issue_number}
```

## Data Contracts

All agents return fenced JSON:

```json
{
  "success": true|false,
  "data": { /* operation results */ },
  "error": null|{
    "code": "ERROR.CODE",
    "message": "Human readable message",
    "recoverable": true|false,
    "suggested_action": "What to do next"
  }
}
```

## Safety

- Pre-flight `gh` CLI auth checks
- Approval gates before destructive operations (unless `--yolo`)
- Test failure prompts
- Actionable error messages with suggested actions
- Worktree isolation prevents contaminating the main working directory

## Integration with sc-git-worktree

The `--fix` workflow creates isolated worktrees via the sc-git-worktree skill:

1. **Create**: `sc-worktree-create` agent creates `fix-issue-{number}` worktree
2. **Implement**: Fix implemented in isolated directory
3. **Commit & Push**: Changes committed and pushed from worktree
4. **Cleanup**: Manual cleanup via `/sc-git-worktree --cleanup` after PR merge

This ensures the main working directory remains clean during fix implementation.

## References

- `references/github-issue-apis.md` - GitHub CLI patterns
- `references/github-issue-checklists.md` - Workflow checklists