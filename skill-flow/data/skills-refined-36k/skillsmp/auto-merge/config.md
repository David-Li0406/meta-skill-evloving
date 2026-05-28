# Auto-Merge Configuration

## Review Settings

| Setting | Value | Description |
|---------|-------|-------------|
| `confidence_threshold` | 60% | Minimum confidence to fix issues |
| `skip_review_for_docs` | true | Skip review pass for docs-only PRs |
| `skip_review_for_config` | true | Skip review pass for config-only PRs |

## CI Settings

| Setting | Value | Description |
|---------|-------|-------------|
| `max_ci_retries` | 3 | Max attempts to fix failing CI |
| `ci_wait_timeout` | 600 | Seconds to wait for CI completion |
| `required_checks` | all | Which checks must pass |

## Merge Settings

| Setting | Value | Description |
|---------|-------|-------------|
| `merge_strategy` | squash | squash, merge, or rebase |
| `delete_branch` | true | Delete branch after merge |
| `update_main_after` | true | Pull main after merge |

## Conflict Handling

| Setting | Value | Description |
|---------|-------|-------------|
| `auto_resolve_conflicts` | simple | none, simple, or aggressive |
| `conflict_file_limit` | 3 | Max files with conflicts to attempt |

### Simple Conflict Resolution

Automatically resolve:
- Package lock file conflicts (regenerate)
- Import order conflicts (take both)
- Whitespace-only conflicts

Abort for:
- Logic changes in same lines
- Structural conflicts
- More than 3 conflicting files

## Comment Handling

| Setting | Value | Description |
|---------|-------|-------------|
| `address_comments` | true | Attempt to address review comments |
| `comment_types` | [suggestion, request] | Types to address |
| `skip_nitpicks` | true | Skip minor style comments |

### Comment Priority

1. **Blocking:** Must address before merge
2. **Request:** Address if straightforward
3. **Suggestion:** Address if clearly beneficial
4. **Nitpick:** Skip unless trivial

## File Patterns

### Files to Skip in Review

```
*.md
*.json (except package.json)
*.yml
*.yaml
.gitignore
LICENSE
```

### Files Requiring Review

```
*.ts
*.tsx
*.js
*.jsx
*.mts
*.mjs
```

## Thresholds

| Metric | Threshold | Action |
|--------|-----------|--------|
| Files changed | > 50 | Warn, continue |
| Lines changed | > 1000 | Warn, continue |
| New files | > 10 | Warn, continue |
| Deleted files | > 5 | Warn, continue |

## Override Flags

Can be passed via command:

```
/auto-merge 91 --skip-review
/auto-merge 91 --no-squash
/auto-merge 91 --keep-branch
```

| Flag | Effect |
|------|--------|
| `--skip-review` | Skip review pass entirely |
| `--no-squash` | Use merge commit instead |
| `--keep-branch` | Don't delete branch |
| `--force` | Skip confirmations |
