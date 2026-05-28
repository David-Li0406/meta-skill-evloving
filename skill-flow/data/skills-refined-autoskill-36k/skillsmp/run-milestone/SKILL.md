---
name: run-milestone
description: Automate milestone development workflow with autopilot PR mode - executes issues from implementation plans, creates PRs, and manages milestone branches
version: 1.0.0
author: Your Team
tags: [development, workflow, automation, milestone, pr]
---

# Run Milestone Skill

## Purpose

This skill automates the execution of development milestones using an autopilot PR workflow. It processes issues from milestone implementation plans, implements them sequentially, creates pull requests, and manages the milestone lifecycle from start to completion.

## When to Use

- Starting work on a new milestone (e.g., M1, M2)
- Continuing work on an in-progress milestone
- Automating the issue-by-issue implementation workflow
- Managing milestone branches and PRs without manual intervention

## Core Workflow

The skill follows this execution pattern:

1. **Bootstrap** - Validate milestone structure and set up base branch
2. **Reconcile** - Check existing PRs and update tracking
3. **Select Next Issue** - Determine which issue to work on next
4. **Execute Issue** - Implement, test, and create PR
5. **Loop** - Continue to next issue until milestone complete

## Input

The skill accepts a milestone identifier:
- Format: `m{n}` (e.g., `m1`, `M1`, or `1`)
- Normalization: Converts to lowercase `m{n}` format
- If missing, prompts user for milestone ID

## Paths and Structure

### Milestone Folder
- Path: `docs/03-build-notes/milestones/<milestone>/`
- Example: `docs/03-build-notes/milestones/m1/`

### Implementation Plan
- Primary: `docs/03-build-notes/milestones/<milestone>/IMPLEMENTATION_PLAN.md`
  - **This file is the source of truth and progress manifest for the milestone**
  - Tracks issue status (✅ Done, ⛔ Needs Review, ⏭️ Skipped)
  - Tracks open PRs and their status
  - Tracks current phase and issue being worked on
  - Tracks blocked issues and stop conditions
  - Always consult and update this file when working on issues
- If missing: STOP and report error

### Epic (Optional)
- Path: `docs/03-build-notes/milestones/<milestone>/00-epic.md`

### Issue Specs
- Pattern: `docs/03-build-notes/milestones/<milestone>/*.md`
- Exclude: `IMPLEMENTATION_PLAN.md`, `00-epic.md`

## Required Context Files

Always load these files before starting work:
- `docs/guides/implementation-workflow.md`
- `docs/guides/dev-cadence.md`

## Autopilot Policy

**Default behavior (no explicit approvals required):**
- One issue → one feature branch → one PR (always)
- Always open PR (never commit directly to base branch)
- Attempt to enable auto-merge after opening PR
- Stop ONLY on "Hard Stop Conditions" (see below - Soft Stops skip automatically)
- **GitHub issue numbers are the source of truth for naming conventions** (branches, commits, PRs)

## Stop Conditions

### Hard Stops (Require User Attention - Workflow Pauses)

When any of these occur, **STOP work on that issue**, **alert the user**, and **wait for user action** before continuing:

1. **Database Changes**
   - Any DB migration or schema change is introduced or modified
   - STOP and alert (requires manual review)
   - Record in "Blocked / Needs Review" section

2. **Sensitive Code Changes**
   - Auth, permissions, rate-limit, or billing code is touched
   - STOP and alert (requires manual review)
   - Record in "Blocked / Needs Review" section

3. **Dependency Changes**
   - Any dependency, lockfile, or license-related change is made
   - STOP and alert (requires manual review)
   - Record in "Blocked / Needs Review" section

4. **Issue Spec Problems**
   - Issue spec is missing, ambiguous, or dependencies are unclear
   - STOP and ask for clarification
   - Record in "Blocked / Needs Review" section

### Soft Stops (Skip Issue Automatically - Workflow Continues)

When any of these occur, attempt auto-fix if applicable, then **skip to next eligible issue** without prompting:

1. **Test Failures**
   - Any required tests fail
   - **Action:** Review test output, attempt reasonable fixes
   - If tests still fail after fixes: Skip to next issue
   - Record in "Blocked / Needs Review" section with reason

2. **Large Diff**
   - >8 files changed OR >400 lines added+removed
   - **Action:** Log warning, skip to next issue immediately
   - Record in "Blocked / Needs Review" section with note about size

3. **Merge Conflicts**
   - Hit merge conflicts or rebase complexity that cannot be resolved safely
   - **Action:** Skip to next issue immediately
   - Record conflict details in "Blocked / Needs Review" section

## Execution Steps

### 1. Bootstrap (Once Per Run)

1. **Resolve milestone identifier**
   - Accept: `m{n}`, `M{n}`, or `{n}` → normalize to `m{n}`
   - If missing, ask user for milestone ID

2. **Verify milestone folder exists**
   - Check: `docs/03-build-notes/milestones/<milestone>/`
   - If missing: STOP with error

3. **Open Implementation Plan**
   - Read: `docs/03-build-notes/milestones/<milestone>/IMPLEMENTATION_PLAN.md`
   - If missing: STOP with missing path error

4. **Determine base branch**
   - Read "Milestone Branch:" from Implementation Plan
   - If present: `base_branch = that value`
   - Else: `base_branch = main`

5. **Ensure base branch exists**
   - Check if branch exists locally and on origin
   - If missing: create from `main` and push
   ```bash
   git checkout -b <base_branch> main
   git push origin <base_branch>
   ```

### 2. Reconcile (Each Run)

1. **List open PRs**
   - Find PRs targeting `base_branch` where title contains `(<milestone>)` or `feat(<milestone>)`
   - Note existing PRs for tracking purposes

2. **Update tracking**
   - If any PRs are merged, update Implementation Plan checkboxes
   - Map PR → issue if confident (check PR title/body for issue numbers)

### 3. Select Next Issue

1. **Determine next eligible issue**
   - Priority order: P0 then P1
   - Top-to-bottom in Implementation Plan
   - Skip issues blocked by unmet dependencies
   - Skip issues already ✅ Done
   - Skip issues ⛔ Needs Review (STOP) unless user explicitly clears them

2. **Identify issue spec file**
   - Use Implementation Plan's "Issue File" column
   - Path: `docs/03-build-notes/milestones/<milestone>/<issue-file>`
   - If missing/ambiguous: STOP and ask

### 4. Execute Issue (No Approval Gates)

1. **Sync base branch**
   ```bash
   git checkout <base_branch>
   git pull origin <base_branch>
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feat/<milestone>-<issue-number>-<short-slug>
   ```

3. **Read issue spec**
   - Read: `docs/03-build-notes/milestones/<milestone>/<issue-file>`
   - Understand acceptance criteria, implementation notes, test expectations

4. **Implement per spec**
   - Write code following issue specifications
   - Write tests alongside implementation
   - Run incremental tests while working

5. **Run full checks (required before PR)**
   - If tests fail: Attempt reasonable fixes, then re-run
   - If tests still fail after fixes: Skip to next issue (soft stop)
   - Record in "Blocked / Needs Review" section with failure reason

6. **Check diff size (before committing)**
   ```bash
   git diff --stat <base_branch>
   ```
   - If >8 files changed OR >400 lines added+removed: Soft stop
   - Log warning, skip to next issue

7. **Commit with proper message**
   ```
   {type}(m{n}): {brief description}

   Implements issue #<ISSUE_NUMBER>: <ISSUE_TITLE>

   - {change 1}
   - {change 2}

   Closes #<ISSUE_NUMBER>
   ```

8. **Push branch**
   ```bash
   git push origin feat/<milestone>-<issue-number>-<short-slug>
   ```

9. **Create PR targeting base branch**
   ```bash
   gh pr create \
     --title "feat(m{n}): <ISSUE_TITLE> (#<ISSUE_NUMBER>)" \
     --base "<base_branch>" \
     --body "..."
   ```

10. **Attempt to enable auto-merge**
    ```bash
    gh pr merge --auto --squash --delete-branch
    ```

### 5. Update Implementation Plan

1. **Add PR entry**
   - Update "Open PRs (autopilot)" section
   - Format: Issue #, PR link, status (checks pending/green)

2. **Update current issue**
   - Update "Current Issue" to next planned issue
   - Update "Current Phase" if phase changed

### 6. Loop

- Proceed to next issue unless a Hard Stop Condition is hit
- For Soft Stops: Skip issue and continue automatically
- For Hard Stops: Wait for user action before continuing
- Continue until all issues complete or milestone blocked by Hard Stop

## Milestone Completion

When all issues are complete:

1. **Verify all issues closed**
2. **Run full CI**
3. **Run integration tests (if applicable)**
4. **Verify epic acceptance criteria**
5. **Create final PR (if using milestone branch)**
6. **After merge to main:**
   ```bash
   git tag -a v0.{n}.0 -m "M{n}: {Milestone Title}"
   git push origin v0.{n}.0

   gh milestone close "M{n} - {Milestone Title}"
   ```

## Limitations

- Requires GitHub CLI (`gh`) for PR management
- Requires git access and proper permissions
- Cannot handle complex merge conflicts automatically
- Requires manual review for hard stop conditions only
- Depends on Implementation Plan format consistency

## Error Handling

- **Missing milestone folder:** STOP with clear error message
- **Missing Implementation Plan:** STOP with path to create it
- **Git errors:** Report error and stop current issue
- **PR creation failures:** Report error and stop
- **Test failures:** Attempt fixes, then skip to next issue if still failing (soft stop)

## Notes

- This skill operates in "autopilot" mode - no explicit approvals required
- Always creates PRs, never commits directly to base branch
- Respects dependencies between issues
- Updates Implementation Plan tracking as work progresses
- Follows one-issue-per-PR pattern strictly
