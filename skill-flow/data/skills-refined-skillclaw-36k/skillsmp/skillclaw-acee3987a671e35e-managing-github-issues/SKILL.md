---
name: managing-github-issues
description: Use this skill to manage GitHub issues from listing to fixing and PR creation with clean worktree isolation.
---

# Skill body

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

```yaml
base_branch: main
worktree_root: ../worktrees
github:
  branch_pattern: "fix-issue-{number}"
```

## Data Contracts

All agents return fenced JSON:
```json
{
  "success": true|false,
  "data": { /* operation results */ },
  "error": null|"message"
}
```

## Safety

- Pre-flight `gh` CLI auth checks
- Approval gates before destructive ops (unless `--yolo`)
- Test failure prompts
- Actionable error messages with suggested actions

## Integration with sc-git-worktree

The `--fix` workflow creates isolated worktrees via the sc-git-worktree skill:

1. **Create**: `sc-worktree-create` agent creates `fix-issue-{number}` worktree
2. **Implement**: Fix implemented in isolated directory
3. **Commit & Push**: Changes committed and pushed from worktree
4. **Cleanup**: Worktree removed after PR creation