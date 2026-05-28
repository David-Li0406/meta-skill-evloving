---
name: pr-feedback
description: "Triage and address PR review feedback and CI failures with minimal diffs; use when asked to respond to review comments or fix CI (trigger keywords: PR feedback, review comments, CI failure)."
---

# PR Feedback

## What this skill does
- Collects PR context, review comments, and CI results.
- Plans and applies minimal changes to resolve feedback.
- Uses the gh CLI for PR context, checks, and logs when available.

## When to use it
- Trigger phrases: "PR feedback", "review comments", "address feedback", "CI failure".
- Use when a PR has reviewer requests or failing checks.

## Step-by-step workflow
0) Verify auth and connectivity: `gh auth status`.
   - If auth fails or tokens are invalid, stop and ask the user to re-auth (`gh auth login -h github.com`) or fix `GITHUB_TOKEN`.
   - Note: `GITHUB_TOKEN`/`GH_TOKEN` override keychain auth. If they are invalid, unset them so `gh` can use the keychain login.
   - If the API is unreachable, ask the user to confirm network/proxy access or paste PR details.
1) Confirm PR context with `gh pr view --json number,title,url,baseRefName,headRefName` (use provided PR number or current branch).
2) Gather feedback and CI status: `gh pr checks <pr>` and review comments via `gh api` if needed.
3) Summarize PR intent, scope, and risks; list failing checks and key feedback themes.
4) Validate each comment against current code; mark stale or out-of-scope items.
5) Draft a short action plan and ask for approval before changes.
6) Implement minimal, targeted fixes; avoid scope creep and drive-by refactors.
7) Verify with focused tests; recheck `gh pr checks` when possible.
8) Prepare per-comment responses with evidence and file references.

## CI failure triage (GitHub Actions only)
- Use `gh pr checks <pr> --json name,state,conclusion,detailsUrl` to identify failures.
- If `conclusion` or `detailsUrl` are not supported (older gh), fall back to:
  - `gh pr checks <pr> --json name,state,link,bucket,workflow,startedAt,completedAt`
  - Use `link` as the details URL and `bucket` as a coarse failure signal.
- For GitHub Actions, extract the run id from `detailsUrl` (or `link`) and fetch logs:
  - `gh run view <run-id> --log`
  - If logs are pending, retry or fetch job logs via `gh api /repos/{owner}/{repo}/actions/jobs/{job_id}/logs`
- For external checks (Buildkite, etc.), report the details URL and mark as out of scope.

## When to push back
- The request conflicts with the PR goal or repo patterns.
- The feedback is stale or contradicted by current code/tests.
- The change would require a large refactor without clear benefit.

## Expected outputs / formatting
- Plan for approval (short, ordered checklist).
- Per-comment resolution notes with action and rationale.
- Summary of files touched and tests run.
- CI status or remaining failures.
- Any pushback phrased respectfully with evidence.

## Example prompts
- "Address the review comments on my PR."
- "Fix the CI failures and summarize what changed."
- "Help me respond to reviewer feedback on this PR."
