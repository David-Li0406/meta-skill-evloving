---
name: gh-pr-checks-fix
description: Use this skill to debug and fix failing GitHub Actions checks on a PR, including summarizing failure contexts, detecting merge conflicts, and proposing a fix plan for user approval.
---

# Gh Pr Checks Fix Workflow

## Overview

This skill utilizes `gh` to inspect GitHub PR checks, detect merge conflicts, collect reviewer feedback, and fetch failing GitHub Actions logs. It summarizes failure contexts, proposes a fix plan, and implements changes after user approval. 

Prerequisite: Ensure `gh` is authenticated (e.g., run `gh auth login` once) and verify authentication status with escalated permissions (workflow/repo scopes). If sandboxing blocks `gh auth status`, rerun it with `sandbox_permissions=require_escalated`.

## Inputs

- `repo`: Path inside the repo (default `.`)
- `pr`: PR number or URL (optional; defaults to current branch PR)
- `gh` authentication for the repo host

## Quick Start

- Run the following command to inspect PR checks:
  ```bash
  python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"
  ```
- Add `--json` for machine-friendly output and `--max-review-comments <number>` to limit reviewer comment listings.

## Workflow

1. **Verify gh Authentication**
   - Run `gh auth status` in the repo with escalated scopes after logging in.
   - If unauthenticated, prompt the user to log in.

2. **Resolve the PR**
   - Prefer the current branch PR: `gh pr view --json number,url`.
   - Use a provided PR number or URL if available.

3. **Check Mergeability and Update-Branch Requirements**
   - Run `gh pr view <pr> --json mergeable,mergeStateStatus`.
   - Treat `mergeable=CONFLICTING` or `mergeStateStatus=DIRTY` as conflicts to resolve.
   - Treat `mergeStateStatus=BEHIND` as requiring an "Update Branch".

4. **Collect Reviewer Feedback**
   - Use the bundled script to list review summaries and comments.
   - Determine if any feedback requires action before addressing CI issues.

5. **Inspect Failing Checks (GitHub Actions Only)**
   - Preferred: Run the bundled script to fetch logs and summarize failures.
   - Manual fallback: Use `gh pr checks <pr> --json` to inspect check statuses.

6. **Scope Non-GitHub Actions Checks**
   - If `detailsUrl` is not a GitHub Actions run, report it as external and provide the URL.

7. **Summarize Failures for the User**
   - Provide the failing check name, run URL, and a concise log snippet.

8. **Create a Fix Plan**
   - Use the `plan` skill to draft a concise plan and request user approval.

9. **Implement After Approval**
   - Apply the approved plan, summarize changes, and inquire about opening a PR.

10. **Recheck Status**
    - Suggest re-running tests and `gh pr checks` to confirm the resolution.

## Bundled Resources

### scripts/inspect_pr_checks.py

This script fetches failing PR checks, detects merge conflicts, collects reviewer feedback, and pulls GitHub Actions logs. It exits non-zero when conflicts, update-branch requirements, reviewer-action requirements, or failures remain.

Usage examples:
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "123"`
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "https://github.com/org/repo/pull/123" --json`

## Outputs
- A structured response or artifact appropriate to the skill.

## Constraints
- Redact secrets/PII by default.
- Avoid destructive operations without explicit user direction.

## Validation
- Run relevant checks or scripts when available.
- Fail fast and report errors before proceeding.

## Antipatterns to Avoid
- Changing unrelated code while addressing a CI failure.
- Ignoring the first failure and fixing downstream issues instead.
- Disabling tests to achieve a green status without justification.
- Proceeding without user approval for code changes.