---
name: gh
description: Use the GitHub gh CLI for any GitHub task (PRs, issues, releases, workflows, repo queries).
---

# GH CLI Workflow

## Overview

Use this skill for any GitHub task with the gh CLI (PRs, issues, releases, workflows, repo queries). Key pattern: always request explicit JSON fields and use statusCheckRollup for checks.

## PR SOP (Default)

Prefer a single PR for a coherent, mergeable unit of work. Only stack when the effort is too large for one PR but can be split into focused, reviewable chunks that build on each other. If a ticket/issue is referenced (GitHub issue or external tracker), include it in the PR body and use a GitHub closing keyword when applicable (e.g., `Closes #123`) so the issue auto-closes on merge. Terminology: use `<branch>` for git; if you use jj, substitute the equivalent bookmark name.

1) Create the PR (single or stacked). If using a stack, update the next PR’s base after the lower layer merges:

- Single PR (base on trunk):

```bash
gh pr create --repo <owner>/<repo> --base <trunk-branch> --head <branch> --title "<conventional title>" --body-file <file>
```

- Stacked PR (base on previous layer):

```bash
gh pr create --repo <owner>/<repo> --base <prev-layer-branch> --head <branch> --title "<conventional title>" --body-file <file>
```

- Stack maintenance (after a lower layer merges into trunk):

```bash
gh pr edit <pr-number> --repo <owner>/<repo> --base <trunk-branch>
```

1) Watch checks and fail fast on the first failure:

```bash
gh pr checks <pr-number> --repo <owner>/<repo> --watch --fail-fast
```

1) If a check fails, get the failing checks and logs:

- details URL format: `https://github.com/<owner>/<repo>/actions/runs/<run-id>/job/<job-id>`

```bash
gh pr view <pr-number> --repo <owner>/<repo> \
  --json statusCheckRollup \
  --jq '.statusCheckRollup[] | select(.conclusion=="FAILURE") | {name,detailsUrl}'
```

```bash
gh run view <run-id> --repo <owner>/<repo> --job <job-id> --log
```

1) Fix locally, push a new commit, then repeat the watch step until CI is green.

1) Merge (only with explicit user approval):

- Never merge unless the user explicitly approves.
- Prefer squash when allowed (delete short-lived branches):

```bash
gh pr merge <pr-number> --squash --delete-branch
```

- If squash is not allowed or unknown, ask which method is allowed, then use `--merge` or `--rebase` explicitly (include `--delete-branch`).
- If a merge queue is enabled, do not pass a merge strategy flag:

```bash
gh pr merge <pr-number> --delete-branch
```

## PR Supporting Commands

1) Fetch PR summary + checks (explicit fields only):

```bash
gh pr view <pr-number> --repo <owner>/<repo> \
  --json title,number,state,headRefName,baseRefName,author,mergeable,commits,files,additions,deletions,labels,statusCheckRollup
```

## Pitfalls and Avoidance

- **Do not run `gh pr view` without `--json`.** The default GraphQL selection can request deprecated `projectCards` and trigger a deprecation error.
- **Do not use `--json checks`.** The field is not supported; use `statusCheckRollup` instead.
- **Keep JSON field lists minimal.** If a field causes errors, remove it and retry with a smaller list.
- **Sanity-check PR scope.** Use `gh pr view <pr> --json commits,files --jq '{commits: [.commits[].messageHeadline], files: [.files[].path]}'` to spot unrelated commits/files early.
- **PR body newlines:** `gh pr create/edit --body` does **not** interpret `\n` escapes. Use `--body-file` (including `--body-file -` with a heredoc) or `gh api ... --input -` with JSON to preserve newlines.
- **PR titles must be Conventional Commits.** Format: `type(scope optional)!: subject`. Allowed types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `build`, `ci`, `perf`. If the user provides a non-conforming title, propose a compliant one and confirm before creating/updating the PR.

## Useful Variations

- PR metadata without checks:

```bash
gh pr view <pr-number> --repo <owner>/<repo> \
  --json title,number,state,headRefName,baseRefName,author,mergeable,commits,files,additions,deletions,labels
```

- Filter only failed checks:

```bash
gh pr view <pr-number> --repo <owner>/<repo> \
  --json statusCheckRollup \
  --jq '.statusCheckRollup[] | select(.conclusion=="FAILURE") | {name,detailsUrl}'
```

## Common Tasks

1) Repo snapshot (explicit fields only):

```bash
gh repo view <owner>/<repo> --json name,description,defaultBranchRef,visibility,homepageUrl
```

1) Issues (list or filter):

```bash
gh issue list --repo <owner>/<repo> --json number,title,state,labels,assignees
```

1) Releases (view by tag):

```bash
gh release view <tag> --repo <owner>/<repo> --json name,tagName,createdAt,assets
```

1) Workflows and runs:

```bash
gh workflow list --repo <owner>/<repo>
gh run list --repo <owner>/<repo>
```

## Decision Notes

- If you need project info, avoid classic projects fields; only add project-related fields if required and be prepared for permission or deprecation errors.
- For cross-repo PRs, always pass `--repo` to avoid querying the wrong default repository.
