---
name: gh-fix-ci
description: Use this skill when you need to debug or fix failing GitHub Actions checks on a PR, including creating a fix plan and implementing changes after user approval.
---

# Skill body

## Overview

Use `gh` to locate failing PR checks, fetch GitHub Actions logs for actionable failures, summarize the failure context, and propose a fix plan for implementation after explicit user approval. This skill also checks for merge conflicts and collects reviewer feedback.

## Prerequisites

Ensure `gh` is authenticated (for example, run `gh auth login` once), then run `gh auth status` with escalated permissions (including workflow/repo scopes) so `gh` commands succeed. If sandboxing blocks `gh auth status`, rerun it with `sandbox_permissions=require_escalated`.

## Inputs

- `repo`: path inside the repo (default `.`)
- `pr`: PR number or URL (optional; defaults to current branch PR)
- `gh` authentication for the repo host

## Quick start

- Run the following command to inspect PR checks:
  ```bash
  python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"
  ```
- Add `--json` for machine-friendly output for summarization.

## Workflow

1. **Verify `gh` authentication**:
   - Run `gh auth status` in the repo with escalated scopes (workflow/repo) after running `gh auth login`.
   - If sandboxed auth status fails, rerun the command with `sandbox_permissions=require_escalated` to allow network/keyring access.
   - If unauthenticated, ask the user to log in before proceeding.

2. **Resolve the PR**:
   - Prefer the current branch PR: `gh pr view --json number,url`.
   - If the user provides a PR number or URL, use that directly.

3. **Check mergeability and update-branch requirements**:
   - Run `gh pr view <pr> --json mergeable,mergeStateStatus,baseRefName,headRefName,url`.
   - Treat `mergeable=CONFLICTING` or `mergeStateStatus=DIRTY` as merge conflicts that must be resolved.
   - Treat `mergeStateStatus=BEHIND` as "Update Branch" required because the base branch advanced.

4. **Inspect failing checks (GitHub Actions only)**:
   - Preferred: run the bundled script:
     ```bash
     python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"
     ```
   - Manual fallback:
     - Run `gh pr checks <pr> --json name,state,bucket,link,startedAt,completedAt,workflow`.
     - For each failing check, extract the run id from `detailsUrl` and run:
       ```bash
       gh run view <run_id> --json name,workflowName,conclusion,status,url,event,headBranch,headSha
       ```

5. **Summarize failure context**:
   - Collect and summarize the failure snippets from the logs.
   - Propose a fix plan based on the summarized context.

6. **Implement changes**:
   - After user approval, implement the proposed changes to resolve the failing checks.