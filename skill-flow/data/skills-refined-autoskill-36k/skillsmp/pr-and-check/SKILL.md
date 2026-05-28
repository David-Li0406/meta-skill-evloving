---
name: PR-and-check
description: Use this skill when you are requested to create a PR for a feature branch to develop, or from develop to production.
---

# Instructions

## 1. Validate branch and determine PR target
- Check current branch: `git branch --show-current`
- Determine the PR flow:
  - If on `develop` → create PR to `production`
  - If on `production` → report error and stop (cannot create PR from production)
  - If on any other branch (feature branch) → create PR to `develop`
- Store the target branch for later use

## 2. Check for existing PR
- Check if a PR already exists for this branch to the target:
  - `gh pr list --head <branch-name> --base <target-branch> --json number,url`
- If a PR exists, report the existing PR URL and skip to step 5 (code review)

## 3. Run tests locally
- Run linting first:
  - run: `npm run lint`
  - if linting fails, analyse the failure, report findings, and stop
- Run unit tests:
  - run: `npm test`
  - if tests fail, analyse the failure, report findings, and stop
- Run build to verify compilation:
  - run: `npm run build`
  - if build fails, analyse the failure, report findings, and stop
- Start the OAuth proxy for E2E tests:
  - run: `./scripts/restart-proxy.sh`
  - verify proxy is running: `curl -s http://127.0.0.1:8787/health`
  - if proxy fails to start, report warning but continue (E2E OAuth tests will be skipped)
- Run E2E tests for all example apps:
  - find all example app directories with e2e tests: `for dir in examples/*/; do if [ -d "${dir}e2e" ]; then echo "$dir"; fi; done`
  - for each example app, run from the project root using absolute path: `cd /path/to/project/examples/<app-name> && npx playwright test`
  - if any E2E tests fail, analyse the failure, report findings, and stop
  - report total number of E2E tests passed across all example apps
- Run security review:
  - invoke the `/security-review` skill to analyze code changes for security vulnerabilities
  - if any HIGH severity vulnerabilities are found with confidence >= 8, report findings and stop
  - include security review summary in the PR body

## 4. Create PR
- Get version number for the PR body:
  - `jq -r .version package.json`
- Get list of commits to include:
  - `git log origin/<target-branch>..HEAD --oneline`
- Create a well-formatted PR:
  - use `gh pr create --base <target-branch> --title "<title>" --body "<body>"` with a HEREDOC for the body
  - highlight the changes and the purpose of the branch
  - include test results summary and version number
- Capture the PR number from the output (needed for code review step)
  - the `gh pr create` command outputs the PR URL, extract the number from it

## 5. Monitor code review
- A code review using the workflow claude-code-review.yml was automatically triggered by the PR
- Verify the workflow started:
  - wait 5 seconds, then check: `gh run list --workflow=claude-code-review.yml --limit 1 --json databaseId,status,headBranch`
  - confirm the run is for the correct branch
  - if workflow failed to start, report error and stop
- Poll for completion (check once per minute, max 10 minutes total):
  - Use separate bash commands with `sleep 60 && gh run list --workflow=claude-code-review.yml --limit 1 --json databaseId,status,conclusion`
  - IMPORTANT: Do NOT use complex shell constructs like `for i in {1..10}` as they cause parse errors
  - Make sequential individual bash calls, checking the status after each one
  - If status is "completed", stop polling
- Check the result:
  - if the workflow did not finish within 10 minutes, report timeout and stop
  - view the review: `gh pr view <pr-number> --comments` or check the PR review file artifact
  - if the review includes recommendations to address before merging, summarize the recommendations and stop
  - if the review ended without critical recommendations, summarize the overall comments and stop

## 6. Check all PR status checks
- After code review completes, check all PR status checks (including non-required ones):
  - run: `gh pr checks <pr-number> --json name,state`
  - report the status of each check
  - if any check has state "FAILURE", report which check failed and investigate using:
    - `gh pr checks <pr-number> --json name,state,link` to get the link to the failed check
    - review the workflow logs to understand the failure
  - report any failed checks to the user, even if they are not required for merge
