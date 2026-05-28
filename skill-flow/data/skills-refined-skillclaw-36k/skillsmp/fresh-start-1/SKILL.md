---
name: fresh-start
description: Orient to project structure and load context
argument-hint: [project-directory]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

Orient to a project directory and load context for execution.

## Project Directory

Use the current working directory by default.

If `$1` is provided, treat `$1` as the working directory and read files under `$1` instead.

## Context Detection

Determine working context before validation:

1. Let WORKING_DIR = `$1` if provided, otherwise current working directory

2. If WORKING_DIR matches pattern `*/features/*` (contains `/features/` followed by a feature name):
   - PROJECT_ROOT = parent of parent of WORKING_DIR (e.g., `/project/features/foo` → `/project`)
   - FEATURE_DIR = WORKING_DIR
   - MODE = "feature"

3. Otherwise:
   - PROJECT_ROOT = WORKING_DIR
   - FEATURE_DIR = none
   - MODE = "greenfield"

## Directory Guard (Wrong Directory Check)

Confirm the required files exist:
- `PROJECT_ROOT/AGENTS.md` must exist
- `EXECUTION_PLAN.md` must exist in:
  - FEATURE_DIR (if feature mode)
  - PROJECT_ROOT (if greenfield mode)

- If either is missing:
  - Tell the user this project is not ready for execution yet
  - If they are in the toolkit repo (e.g., `GENERATOR_PROMPT.md` exists), instruct them to:
    1. Run `/generate-plan <project-path>` from the toolkit repo (or `/feature-plan` for features)
    2. `cd` into the project/feature directory
    3. Re-run `/fresh-start`
  - Otherwise, ask the user for the correct project directory path and re-run `/fresh-start <project-path>`

## Git Initialization (First Run)

In PROJECT_ROOT (not the feature directory):

1. Check whether this is already a git repo by running:
   ```bash
   git -C PROJECT_ROOT rev-parse --is-inside-work-tree 2>/dev/null
   ```
   If this returns "true", it's already a git repo.
2. If not a git repo:
   - Ask: "Initialize git in this project now?" (recommended)
   - If yes:
     ```bash
     git init
     git branch -M main
     ```
3. If it is a git repo but has no commits yet:
   - Ask: "Create an initial commit of the current project state now?" (recommended)
   - If yes:
     ```bash
     git add -A
     git commit -m "chore: initial commit"
     ```

## Feature Branch Setup (Feature Mode Only)

If MODE = "feature", create an isolated branch for this feature work:

1. Derive FEATURE_NAME from the feature directory (basename of FEATURE_DIR, e.g., `analytics-dashboard`)

2. Check current branch:
   ```bash
   git branch --show-current
   ```

3. If already on a `feature/FEATURE_NAME` branch, skip (already set up)

4. Otherwise, create and switch to the feature branch:
   ```bash
   # Commit any uncommitted changes first (preserves user work)
   git add -A && git diff --cached --quiet || git commit -m "wip: uncommitted changes before feature/FEATURE_NAME"

   # Create feature branch from current HEAD
   git checkout -b feature/FEATURE_NAME
   ```

5. Report: "Created branch `feature/FEATURE_NAME` for isolated feature development"

## AGENTS_ADDITIONS Merge (Feature Mode Only)

If MODE = "feature", check for and offer to merge workflow additions:

1. Check if `FEATURE_DIR/AGENTS_ADDITIONS.md` exists
   - If not, skip this section

2. Read AGENTS_ADDITIONS.md and determine if merge is needed:
   - If it contains "No additions required" or similar, report: "No AGENTS.md additions needed for this feature" and skip
   - If it contains actual additions, continue to step 3

3. Summarize the additions for the user:
   ```
   AGENTS_ADDITIONS.md proposes workflow additions:

   - {Section Name 1}: {one-line summary of why it's needed}
   - {Section Name 2}: {one-line summary of why it's needed}
   ...
   ```

4. Ask: "Apply these workflow additions to AGENTS.md now? (recommended before starting work)"

5. If user approves:
   - Read current PROJECT_ROOT/AGENTS.md
   - Use AGENTS_ADDITIONS.md as instructions to edit AGENTS.md:
     - Extract the "Content to add" blocks
     - Insert each block at the location specified in "Where to add"
     - If location is unclear, append to end of AGENTS.md
   - Add a comment marker where content was added: `<!-- Added for FEATURE_NAME -->`
   - Prepend a header to AGENTS_ADDITIONS.md indicating merge is complete:
     ```
     <!-- MERGED into PROJECT_ROOT/AGENTS.md on YYYY-MM-DD -->
     ```
   - Report: "Applied workflow additions to AGENTS.md"

6. If user declines:
   - Report: "Skipped. You can manually apply AGENTS_ADDITIONS.md changes later."
   - Continue with fresh-start (don't block)

## Verification Configuration (First Run)

Check if verification is configured:

1. Check if `PROJECT_ROOT/.claude/verification-config.json` exists and is non-empty
2. If it exists and has content, skip this section
3. If missing or empty, check for a `"skipped": true` marker — if present, skip
4. Otherwise, prompt the user:

```
Verification not configured. Configure now?

[Y] Yes - run /configure-verification (recommended)
[n] No - remind me later
[s] Skip - don't ask again for this project
```

**Handling:**
- **Y (default):** Invoke `/configure-verification` with PROJECT_ROOT, then continue
- **n:** Report "Run `/configure-verification` before `/phase-prep` to enable automated verification." and continue
- **s:** Create `.claude/verification-config.json` with `{"skipped": true}` and continue

**Note:** In non-interactive/CI environments, if no response is possible, treat as "n" (remind later) and continue without blocking.

## Required Context

Read these files first:
- **PROJECT_ROOT/AGENTS.md** — Workflow guidelines
- **EXECUTION_PLAN.md** — Tasks and acceptance criteria (from FEATURE_DIR if feature mode, else PROJECT_ROOT)

## Specification Documents

Check which of these exist and read them:

**From PROJECT_ROOT** (always check):
- **PRODUCT_SPEC.md** — What we're building (greenfield)
- **TECHNICAL_SPEC.md** — How it's built (greenfield)
- **LEARNINGS.md** — Discovered patterns and gotchas (if exists)

**From FEATURE_DIR** (if feature mode):
- **FEATURE_SPEC.md** — Feature requirements
- **FEATURE_TECHNICAL_SPEC.md** — Feature technical approach

## Your Task

1. Read all available documents above
2. Summarize your understanding:
   - What is being built
   - Current phase and progress
   - Tech stack and key patterns
   - Key learnings to follow (if LEARNINGS.md exists)
3. Confirm you're ready to begin execution

**Important:** If LEARNINGS.md exists, apply those patterns throughout your work. These are project-specific conventions discovered during development that override general defaults.
