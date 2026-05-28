---
name: gh-fix-ci
description: Use this skill when you need to inspect GitHub PR checks, fetch failing GitHub Actions logs, summarize failure context, and create a fix plan for implementation after user approval.
---

# Gh Pr Checks Plan Fix

## Overview

Use `gh` to locate failing PR checks, detect merge conflicts, collect reviewer feedback, and fetch GitHub Actions logs for actionable failures. Summarize the failure snippet, propose a fix plan, and implement it after explicit approval. This skill depends on the `plan` skill for drafting and approving the fix plan.

Prerequisite: Ensure `gh` is authenticated (for example, run `gh auth login` once), then run `gh auth status` with escalated permissions (including workflow/repo scopes) so `gh` commands succeed. If sandboxing blocks `gh auth status`, rerun it with `sandbox_permissions=require_escalated`.

## Inputs

- `repo`: path inside the repo (default `.`)
- `pr`: PR number or URL (optional; defaults to current branch PR)
- `gh` authentication for the repo host

## Quick start

- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"`
- Add `--json` for machine-friendly output.
- Add `--max-review-comments <number>` to limit reviewer comment listings.

## Workflow

1. **Verify gh authentication.**
   - Run `gh auth status` in the repo with escalated scopes (workflow/repo) after running `gh auth login`.
   - If sandboxed auth status fails, rerun the command with `sandbox_permissions=require_escalated` to allow network/keyring access.
   - If unauthenticated, ask the user to log in before proceeding.

2. **Resolve the PR.**
   - Prefer the current branch PR: `gh pr view --json number,url`.
   - If the user provides a PR number or URL, use that directly.

3. **Check mergeability and collect reviewer feedback.**
   - Inspect for merge conflicts and update-branch requirements using:
     - `gh pr view <pr> --json mergeable,mergeStateStatus,baseRefName,headRefName,url`
   - Collect reviewer feedback using the bundled script to list review summaries, inline review comments, and issue comments.

4. **Inspect failing checks (GitHub Actions only).**
   - Preferred: run the bundled script:
     - `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"`
   - Manual fallback:
     - `gh pr checks <pr> --json name,state,bucket,link,startedAt,completedAt,workflow`
     - For each failing check, extract the run id from `detailsUrl` and run:
       - `gh run view <run_id> --json name,workflowName,conclusion,status,url,event,headBranch,headSha`
       - `gh run view <run_id> --log`
     - If the run log says it is still in progress, fetch job logs directly:
       - `gh api "/repos/<owner>/<repo>/actions/jobs/<job_id>/logs" > "<path>"`

5. **Scope non-GitHub Actions checks.**
   - If `detailsUrl` is not a GitHub Actions run, label it as external and only report the URL.

6. **Summarize failures for the user.**
   - Provide the failing check name, run URL (if any), and a concise log snippet.
   - Call out missing logs explicitly.

7. **Create a plan.**
   - Use the `plan` skill to draft a concise plan and request approval.

8. **Implement after approval.**
   - Apply the approved plan, summarize diffs/tests, and ask about opening a PR.

9. **Recheck status.**
   - After changes, suggest re-running the relevant tests and `gh pr checks` to confirm.

## Bundled Resources

### scripts/inspect_pr_checks.py

Fetch failing PR checks, pull GitHub Actions logs, and extract a failure snippet. Exits non-zero when failures remain so it can be used in automation.

Usage examples:
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "123"`
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "https://github.com/org/repo/pull/123" --json`
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --max-lines 200 --context 40`