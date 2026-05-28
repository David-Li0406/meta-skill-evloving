---
name: glab
description: Query and manage GitLab merge requests, pipelines, and issues using glab CLI for EFG TECH project. READ-ONLY by default - always ask user approval before creating, merging, or modifying MRs/issues.
license: MIT
compatibility: opencode
---

# GitLab CLI Skill (EFG TECH Project)

Query and manage GitLab for CI/CD pipeline monitoring, issue tracking, and merge request inspection using the `glab` CLI. This skill is READ-ONLY by default.

## CRITICAL RULES

### READ-ONLY BY DEFAULT

**NEVER execute state-changing commands without explicit user approval.**

Allowed without asking:
- `glab mr list`, `glab mr view`, `glab mr diff`
- `glab pipeline list`, `glab pipeline view`, `glab pipeline status`
- `glab issue list`, `glab issue view`
- `glab ci status`, `glab ci view`
- `glab repo view`
- `glab auth status`
- Any `--json` query or inspection command

**MUST ASK USER BEFORE (state-changing):**
- `glab mr create`, `glab mr merge`, `glab mr close`, `glab mr update`, `glab mr approve`
- `glab issue create`, `glab issue close`, `glab issue update`
- `glab pipeline run`, `glab pipeline retry`, `glab pipeline cancel`
- `glab mr comment`, `glab issue comment`
- Any command that creates, modifies, or deletes resources

### Approval Request Format

Before any state-changing operation, ask:

```
I need to run a state-changing GitLab command:
  Command: glab mr merge 123 --squash
  Impact: Will merge MR !123 into target branch
  Project: eslfaceitgroup/technology/faceit/protos

Do you approve? (yes/no)
```

## Prerequisites

- `glab` CLI installed
- Authenticated: `glab auth status`
- Repository context (run from repo directory or use `--repo` flag)

## Quick Reference (Read-Only)

### Authentication & Config

```bash
# Check auth status
glab auth status

# View current repo context
glab repo view

# Set default repo (if not in repo directory)
glab config set -g default_repo eslfaceitgroup/technology/faceit/<repo>
```

---

## EFG Organization Structure

```
eslfaceitgroup/
├── technology/
│   └── faceit/
│       ├── protos           # Protocol buffer definitions
│       ├── user-api         # User service
│       ├── auth-api         # Authentication service
│       └── ...              # Other services
```

### Common Repo Paths

```bash
# Protos repository
eslfaceitgroup/technology/faceit/protos

# Use with --repo flag when outside repo directory
glab mr list --repo eslfaceitgroup/technology/faceit/protos
```

---

## Branch Naming Convention

Use the format: `<JIRA-TICKET>/<description>`

```bash
# Examples
TECH-5420/add-password-field
TECH-1234/fix-auth-bug
TECH-9999/update-user-proto
```

---

## Merge Requests - Read-Only Commands

### List Merge Requests

```bash
# List open MRs
glab mr list

# List all MRs (including merged/closed)
glab mr list --state all

# List merged MRs
glab mr list --state merged

# List my MRs
glab mr list --author @me

# List MRs assigned to me for review
glab mr list --reviewer @me

# List MRs by label
glab mr list --label "needs-review"

# List MRs targeting specific branch
glab mr list --target-branch main

# JSON output
glab mr list --output json
```

### View Merge Request

```bash
# View MR details
glab mr view <mr-number>

# View in browser
glab mr view <mr-number> --web

# View MR diff
glab mr diff <mr-number>

# View MR with comments
glab mr view <mr-number> --comments

# Check MR pipeline status
glab mr view <mr-number> --output json | jq '.pipeline'
```

### Create Merge Request (REQUIRES APPROVAL)

```bash
# Create MR interactively - ASK APPROVAL FIRST
glab mr create

# Create with title and description - ASK APPROVAL FIRST
glab mr create --title "feat: add feature X" --description "Description..."

# Create with target branch - ASK APPROVAL FIRST
glab mr create --title "Fix bug" --target-branch main

# Create draft MR - ASK APPROVAL FIRST
glab mr create --title "WIP: Feature" --draft

# Create with labels - ASK APPROVAL FIRST
glab mr create --title "Feature" --label enhancement

# Create with assignee - ASK APPROVAL FIRST
glab mr create --title "Feature" --assignee username

# Create from description file - ASK APPROVAL FIRST
glab mr create --title "Feature X" --description "$(cat description.md)"

# Fill from commit messages - ASK APPROVAL FIRST
glab mr create --fill
```

### Update Merge Request (REQUIRES APPROVAL)

```bash
# Add comment - ASK APPROVAL FIRST
glab mr comment <mr-number> --message "LGTM!"

# Update title - ASK APPROVAL FIRST
glab mr update <mr-number> --title "New title"

# Add labels - ASK APPROVAL FIRST
glab mr update <mr-number> --label "ready-for-review"

# Mark as ready (from draft) - ASK APPROVAL FIRST
glab mr update <mr-number> --ready

# Add assignee - ASK APPROVAL FIRST
glab mr update <mr-number> --assignee username

# Add reviewer - ASK APPROVAL FIRST
glab mr update <mr-number> --reviewer username
```

### Review Merge Request (REQUIRES APPROVAL)

```bash
# Approve MR - ASK APPROVAL FIRST
glab mr approve <mr-number>

# Unapprove MR - ASK APPROVAL FIRST
glab mr revoke <mr-number>
```

### Merge (REQUIRES APPROVAL)

```bash
# Merge MR - ASK APPROVAL FIRST
glab mr merge <mr-number>

# Squash merge - ASK APPROVAL FIRST
glab mr merge <mr-number> --squash

# Merge and delete source branch - ASK APPROVAL FIRST
glab mr merge <mr-number> --remove-source-branch

# Merge when pipeline succeeds - ASK APPROVAL FIRST
glab mr merge <mr-number> --when-pipeline-succeeds
```

### Checkout MR Locally (Safe - Local Only)

```bash
# Checkout MR branch
glab mr checkout <mr-number>

# Checkout and create local branch
glab mr checkout <mr-number> --branch my-local-branch
```

---

## CI/CD Pipelines - Read-Only Commands

### List Pipelines

```bash
# List recent pipelines
glab pipeline list

# List pipelines for specific branch
glab pipeline list --branch main

# List pipelines with status
glab pipeline list --status failed
glab pipeline list --status success
glab pipeline list --status running

# JSON output
glab pipeline list --output json
```

### View Pipeline Details

```bash
# View pipeline status
glab pipeline status

# View specific pipeline
glab pipeline view <pipeline-id>

# View pipeline in browser
glab pipeline view <pipeline-id> --web

# View CI status for current branch
glab ci status
```

### View Pipeline Jobs

```bash
# List jobs for a pipeline
glab ci list

# View job logs
glab ci view <job-id>

# View job trace/logs
glab ci trace <job-id>
```

### Pipeline Actions (REQUIRES APPROVAL)

```bash
# Retry failed pipeline - ASK APPROVAL FIRST
glab pipeline retry <pipeline-id>

# Cancel running pipeline - ASK APPROVAL FIRST
glab pipeline cancel <pipeline-id>

# Run new pipeline - ASK APPROVAL FIRST
glab pipeline run

# Run pipeline on specific branch - ASK APPROVAL FIRST
glab pipeline run --branch feature-branch

# Run with variables - ASK APPROVAL FIRST
glab pipeline run --variables "VAR1:value1,VAR2:value2"
```

---

## Issues - Read-Only Commands

### List Issues

```bash
# List open issues
glab issue list

# List all issues
glab issue list --state all

# List closed issues
glab issue list --state closed

# List issues assigned to me
glab issue list --assignee @me

# List issues by label
glab issue list --label bug

# Search issues
glab issue list --search "memory leak"

# JSON output
glab issue list --output json
```

### View Issue

```bash
# View issue details
glab issue view <issue-number>

# View in browser
glab issue view <issue-number> --web

# View with comments
glab issue view <issue-number> --comments
```

### Create Issue (REQUIRES APPROVAL)

```bash
# Create issue interactively - ASK APPROVAL FIRST
glab issue create

# Create with title and description - ASK APPROVAL FIRST
glab issue create --title "Bug: Application crashes" --description "Steps..."

# Create with labels - ASK APPROVAL FIRST
glab issue create --title "Fix login" --label bug --label urgent

# Create with assignee - ASK APPROVAL FIRST
glab issue create --title "Feature X" --assignee username
```

### Update Issue (REQUIRES APPROVAL)

```bash
# Add comment - ASK APPROVAL FIRST
glab issue comment <issue-number> --message "Working on this"

# Close issue - ASK APPROVAL FIRST
glab issue close <issue-number>

# Reopen issue - ASK APPROVAL FIRST
glab issue reopen <issue-number>

# Update labels - ASK APPROVAL FIRST
glab issue update <issue-number> --label "in-progress"
```

---

## Repository Information (Read-Only)

```bash
# View repo info
glab repo view

# View in browser
glab repo view --web

# Clone repo
glab repo clone eslfaceitgroup/technology/faceit/<repo>

# List branches
glab api projects/:id/repository/branches --paginate | jq '.[].name'

# List tags
glab release list
```

---

## Common Workflows

### Create Feature Branch and MR

```bash
# 1. Create branch from JIRA ticket
git checkout -b TECH-1234/feature-description

# 2. Make changes and commit
git add .
git commit -m "feat: add feature description

TECH-1234"

# 3. Push branch
git push -u origin TECH-1234/feature-description

# 4. Create MR - ASK APPROVAL FIRST
glab mr create --title "feat: add feature description" \
  --description "## Summary\n\nDescription here\n\n## JIRA\n\nTECH-1234" \
  --target-branch master
```

### Check MR Pipeline Status

```bash
# View MR with pipeline info
glab mr view <mr-number>

# Check CI status
glab ci status

# View failed job logs
glab ci trace <job-id>
```

### Review and Merge MR

```bash
# 1. View MR details (read-only)
glab mr view <mr-number>

# 2. View diff (read-only)
glab mr diff <mr-number>

# 3. Approve - ASK APPROVAL FIRST
glab mr approve <mr-number>

# 4. Merge - ASK APPROVAL FIRST
glab mr merge <mr-number> --squash --remove-source-branch
```

---

## Debugging CI/CD Failures (Read-Only)

### Quick Diagnosis Workflow

```bash
# 1. Check current pipeline status
glab ci status

# 2. List recent failed pipelines
glab pipeline list --status failed

# 3. View pipeline details
glab pipeline view <pipeline-id>

# 4. View failed job logs
glab ci trace <job-id>
```

---

## API Access (Read-Only)

```bash
# Get project info
glab api projects/:id

# Get MR details
glab api projects/:id/merge_requests/<mr-iid>

# Get pipeline details
glab api projects/:id/pipelines/<pipeline-id>

# List project members
glab api projects/:id/members
```

---

## Safety Checklist

Before ANY state-changing operation:

1. [ ] Is this a read-only command? If yes, proceed. If no, continue checklist.
2. [ ] Have I asked the user for explicit approval?
3. [ ] Did the user say "yes" or approve the specific command?
4. [ ] Verified correct repository context
5. [ ] Understood the impact (what will be created/modified/deleted)

### State-Changing Commands Summary

| Category | Commands Requiring Approval |
|----------|---------------------------|
| MRs | `mr create`, `mr merge`, `mr close`, `mr update`, `mr approve`, `mr comment` |
| Issues | `issue create`, `issue close`, `issue update`, `issue comment` |
| Pipelines | `pipeline run`, `pipeline retry`, `pipeline cancel` |
| CI Jobs | `ci retry` |

---

## Troubleshooting

### "Not authenticated"

```bash
glab auth login
glab auth status
```

### "Project not found"

- Check project path is correct
- Use `--repo eslfaceitgroup/technology/faceit/<repo>` flag
- Verify you have access to the project

### "Pipeline failed"

```bash
# Check pipeline status
glab pipeline status

# View failed job logs
glab ci list
glab ci trace <failed-job-id>
```

### "MR cannot be merged"

- Check for merge conflicts: `glab mr view <mr-number>`
- Check pipeline status: `glab ci status`
- Check approvals: `glab mr view <mr-number> --output json | jq '.approvals_required'`

---

## Quick Reference Card

### Read-Only (Always Safe)

```bash
glab auth status                     # Check auth
glab repo view                       # Repo info
glab mr list                         # List MRs
glab mr view <mr-number>             # View MR
glab mr diff <mr-number>             # View diff
glab pipeline list                   # List pipelines
glab ci status                       # CI status
glab issue list                      # List issues
glab issue view <issue-number>       # View issue
```

### State-Changing (Always Ask First)

```bash
glab mr create --title "..." --description "..."    # Create MR
glab mr merge <mr-number>                           # Merge MR
glab mr approve <mr-number>                         # Approve MR
glab mr comment <mr-number> --message "..."         # Comment
glab pipeline run                                   # Run pipeline
glab pipeline retry <pipeline-id>                   # Retry pipeline
glab issue create --title "..."                     # Create issue
```
