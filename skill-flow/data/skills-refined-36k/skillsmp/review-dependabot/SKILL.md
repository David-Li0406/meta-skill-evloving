---
name: review-dependabot
description: Merge Dependabot PRs, update dependencies, handle dependency updates. Use when Dependabot PRs are pending, need to review dependency bumps, or update packages safely.
disable-model-invocation: true
context: fork
---

# Review Dependabot

Analyze open Dependabot PRs and merge safe updates.

## Workflow

1. Fetch all open Dependabot PRs
2. Categorize by safety level and merge constraints
3. Present summary table with recommendations
4. Use AskUserQuestion for batch approval
5. Merge approved PRs, handle failures gracefully

## Fetching PRs

**Single repo:**

```bash
gh pr list --author app/dependabot --state open --json number,title,body,url,statusCheckRollup,files
```

**Multi-repo** (when user mentions "all repos", specifies an owner, or cwd has no git repo):

```bash
gh search prs --author app/dependabot --owner {owner} --state open --json repository,number,title,url
```

For each repo, check `~/Repos/` for existing clone or clone to `/tmp/dependabot-review/{repo-name}`, then fetch full details with `gh pr view`.

## PR Categories

### Safe to Merge

PRs mergeable immediately (CI passing, status `MERGEABLE`):

- **Patch versions** (`1.2.3 → 1.2.4`) - bug fixes only
- **`@types/*` packages** - type definitions, no runtime code
- **Security patches** - PR body mentions CVE or advisory
- **Dev dependencies (minor)** - build-time only

### Manual Merge Required

PRs modifying `.github/workflows/*` require the `workflow` OAuth scope (unavailable to `gh` CLI). Check the `files` field, present GitHub URLs, and let the user merge via browser.

### Needs Review

Major bumps (`3.x → 4.x`), runtime dependencies, and framework updates warrant deeper analysis. Spawn `general-purpose` agents in parallel:

```
Evaluate {name} {old} → {new} for {repo}:

1. Search for "{name} v{new_major} migration guide"
2. Extract breaking changes from PR body (release notes)
3. Search codebase for usage: `rg "{name}"`
4. Assess impact on found usages

Response: Confidence (0-100%), breaking changes, migration URL, recommendation (merge/review/skip), one-sentence reason.
```

### Skip

- **CI failing** - note if related to the update or pre-existing
- **Merge conflicts** (`CONFLICTING`) - needs Dependabot rebase

## Summary Presentation

Group PRs by category with tables. Formatting notes:

- Include counts in headers: "Safe to Merge (6 PRs)"
- Use tables for Safe/Needs Review/Skipped categories
- Use bullet list with inline GitHub URLs for Manual Merge Required
- Tailor columns per category (e.g., Confidence/Issue for Needs Review, Reason for Skipped)

## User Decision

Use AskUserQuestion: (1) Merge all safe PRs, (2) Include manual-merge PRs (opens browser tabs), (3) Select individually, (4) Cancel.

## Merge Execution

```bash
gh pr merge {number} --squash
```

### Handling Failures

**Lockfile conflicts**: Merge PRs sequentially per repo. When a merge fails with "not mergeable", comment `@dependabot rebase` and inform the user.

**Workflow file errors** ("refusing to allow an OAuth App to create or update workflow"): Move to Manual Merge Required list with GitHub URL.

## Detection Patterns

Identify PR types from title patterns:

| Title Pattern      | Category                                  |
| ------------------ | ----------------------------------------- |
| `Bump @types/`     | TypeScript types (safe)                   |
| `Bump actions/`    | GitHub Actions (check for workflow files) |
| `group` in title   | Grouped update (evaluate each dependency) |
| `security` in body | Security patch (prioritize)               |
| `CVE-` in body     | Security patch (prioritize)               |
| `x.0.0` in version | Major bump (needs review)                 |
