---
name: github-pr-flow
description: manage branches and full pull request lifecycle, from creation to merge
metadata:
  category: github
---

# GitHub PR Flow

## What is it?

The **PR Flow Skill** handles the logistics of code contribution: creating branches, opening Pull Requests, synchronizing branches, and merging.

## Success Criteria

- Branch exists before PR creation.
- PR titles follow [Conventional Commits](../github-kernel/references/CONVENTIONAL_COMMITS.md).
- PR description clearly states the changes using structured format.
- Branch synchronization performed before review and merge.
- Merges use appropriate strategy (squash/merge/rebase).
- Approvals and checks verified before merging.
- Security fixes include CVE references and priority indicators.

## Why use it?

- **Streamlined contribution workflow**: Manage the complete PR lifecycle from branch to merge
- **Convention enforcement**: Ensures PR titles and descriptions follow team standards
- **Conflict prevention**: Handles branch synchronization to avoid merge conflicts
- **Flexible merge strategies**: Supports squash, merge, and rebase workflows
- **Safe collaboration**: Validates approvals and checks before merging

## When to use this skill

- "Create a new branch for feature X."
- "Open a PR for my current changes."
- "Update this PR branch with the latest main."
- "Merge PR #50."
- "Create a hotfix branch from release/v2.1."
- "Update PR title to follow conventional commits."
- "Create PRs targeting both release and main branches."

## What this skill can do

- **Branch Management**: Create feature/hotfix branches from any base (main, release, etc.).
- **PR Creation**: Open Draft PRs with structured descriptions.
- **PR Updates**: Modify titles, descriptions, base branches, draft status, and reviewers.
- **Branch Synchronization**: Update PR branches with latest base changes via `update_pull_request_branch`.
- **Multi-Target PRs**: Create multiple PRs from same branch (e.g., hotfix to release and main).

## What this skill will NOT do

- Review code (use `github-review-cycle`).
- Modify file contents (use `github-kernel` tools like `create_or_update_file`).
- Run CI/CD checks (it only views status).

## How to use this skill

1. **Branch**: Always start by ensuring a branch exists before creating a feature branch from main (`create_branch`).
2. **Commit**: Make changes via file editing tools (see `github-kernel`).
3. **PR**: Create PR with structured description (`create_pull_request`).
4. **Sync**: Update branch before review/merge (`update_pull_request_branch`).
5. **Review**: Request reviews (use `github-review-cycle` skill).
6. **Merge**: Execute merge with appropriate strategy (`merge_pull_request`).


### Branch Synchronization

**When to sync:**
- Before requesting review (ensure up-to-date with base)
- Before merging (required for clean merge)
- When base branch has moved ahead significantly
- After resolving conflicts locally

**Sync responses:**
- ✅ Success: Branch updated with latest base changes
- ℹ️ 422 Error: Already up-to-date (no action needed)
- ❌ Conflict: Manual resolution required
## Tool usage rules

### PR Title Conventions

All PR titles MUST follow [Conventional Commits](../github-kernel/references/CONVENTIONAL_COMMITS.md):

- `feat:` New features
- `fix:` Bug fixes  
- `docs:` Documentation changes
- `refactor:` Code restructuring
- `test:` Test additions/changes
- `chore:` Maintenance tasks
- `perf:` Performance improvements
- `ci:` CI/CD changes

**Examples:**
- ✅ `feat: implement OAuth2 authentication`
- ✅ `fix: critical security patch for CVE-2026-1234`
- ❌ `Updates to login` (no type prefix)
- ❌ `Feature/new-ui` (not conventional format)

### PR Description Structure

Use structured format for clarity:

```markdown
## Description
[Clear summary of what and why]

## Changes
- Specific change 1
- Specific change 2

## Testing
[How changes were verified]

## Impact
[Breaking changes, dependencies, deployment notes]
```

**Security PRs must include:**
- CVE reference (if applicable)
- Severity level (Critical/High/Medium/Low)
- Affected components
- Mitigation approach

### Branch Operations

- **Creation**: `create_branch` with explicit `from_branch` parameter
- **Hotfix**: Always specify release branch as base
- **Naming**: Use prefixes: `feat/`, `fix/`, `hotfix/`, `docs/`, `refactor/`

### PR Lifecycle

- **Draft → Ready**: Use `update_pull_request` with `draft: false`
- **Update Metadata**: `update_pull_request` (title, body, base, reviewers)
- **Sync Branches**: `update_pull_request_branch` (git-level sync)
- **Close**: `update_pull_request` with `state: closed`

### Merge Strategy Decision Tree

**Squash (`squash`):**
- ✅ Feature branches with multiple WIP commits
- ✅ Clean single commit in history desired
- ✅ Individual contributor branches
- Example: Feature development with 15 commits → 1 clean commit

**Merge (`merge`):**
- ✅ Release branches merging to main
- ✅ Preserving detailed commit history required
- ✅ Multiple contributors with meaningful commits
- Example: Hotfix branch with verified commits

**Rebase (`rebase`):**
- ✅ Linear history required
- ✅ Few clean commits already
- ✅ No merge commits desired
- Example: Small fixes with 1-2 commits

## Examples

See [references/examples.md](references/examples.md) for compliant PR flow examples.

## Error Handling

### Common Scenarios

**404 Not Found**
- Branch/PR doesn't exist
- **Action**: Verify branch name, create if needed

**422 Unprocessable**
- Branch already up-to-date during sync
- **Action**: No action needed, proceed with review/merge

**Base branch doesn't exist**
- Creating PR with non-existent base
- **Action**: Create base branch first or verify target

**Merge conflicts**
- Cannot auto-merge due to conflicts
- **Action**: Resolve conflicts locally, push, then retry

**Branch protection violations**
- Attempting to merge without approvals/checks
- **Action**: Wait for required approvals and CI to pass

## Cross-References

- **File Operations**: Use [`github-kernel`](../github-kernel/SKILL.md) for creating/updating files before PR
- **Code Review**: Use [`github-review-cycle`](../github-review-cycle/SKILL.md) for requesting and submitting reviews
- **Commit Standards**: Follow [Conventional Commits](../github-kernel/references/CONVENTIONAL_COMMITS.md)

## Limitations

- Cannot resolve merge conflicts automatically (requires manual or file-edit intervention).
- Cannot bypass branch protection rules.
- Cannot modify files directly (use `github-kernel` for file operations).
- Cannot run or control CI/CD pipelines (only view status).
