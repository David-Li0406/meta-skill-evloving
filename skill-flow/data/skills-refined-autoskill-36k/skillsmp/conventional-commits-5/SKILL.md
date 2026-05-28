---
name: conventional-commits
description: Use this skill ONLY for 'commit', 'save', or 'finish' prompts. Enforces strict manual approval, intelligent Topic-to-Global branching, and sync automation.
---

# Mandatory Commit & Safety Protocol

## 1. Two-Tier Branching & Intelligent Naming (MANDATORY)
- **Zero-Commit Rule for Main:** Never commit directly to `main` or `master`.
- **Local Topic Phase (Development):**
    1. If on `main`, analyze changes to propose a `topic/` name (e.g., `topic/fix-nutrition-logic`) and switch.
    2. Commit atomic changes locally on these topic branches.
- **Global Feature Phase (Remote Push):**
    1. When the user is ready to push, analyze all unmerged `topic/` branches to propose a summarizing `feature/` name (e.g., `feature/mvp-nutrition-engine`).
    2. Automatically merge active `topic/` branches into this Global Feature branch using `scripts/git_sync.sh`.
    3. Push the Global Feature branch to remote (origin).

## 2. Pre-Commit Review (Required)
- Before proposing any commit, you **MUST** execute: `bash ./scripts/review.sh`.
- You must display the output of this script to the user for verification.

## 3. Explicit Commit Types
All commit messages must strictly follow the format: `<type>(<scope>): <description>`
- **feat**: A new feature.
- **fix**: A bug fix.
- **docs**: Documentation changes.
- **style**: Formatting/styling (no code change).
- **refactor**: Code refactoring.
- **perf**: Performance improvements.
- **test**: Adding/refactoring tests.
- **chore**: Build/maintenance tasks.

## 4. Mandatory Consent (The Barrier)
- **STOP and WAIT:** After showing the review and proposed branch/message, you are strictly forbidden from executing `git commit` or `git merge`.
- Ask: "I have prepared the commit on [branch-name]. Should I proceed?"
- Only proceed if the user says "Yes", "Go", or "Proceed".
