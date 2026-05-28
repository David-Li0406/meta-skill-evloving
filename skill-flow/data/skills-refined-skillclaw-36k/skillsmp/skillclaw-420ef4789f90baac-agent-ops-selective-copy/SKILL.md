---
name: agent-ops-selective-copy
description: Use this skill when you need to create clean git branches from feature work while excluding specific agent-ops files for pull request preparation.
---

# Selective Copy — Clean Branch Creation

> Create a clean git branch from feature work, excluding specific paths. Platform agnostic.

**Works with or without `aoc` CLI.** Uses standard git commands.

---

## Purpose

Create a new branch containing feature work while excluding agent/workflow files for clean PRs.

---

## CRITICAL: No Assumptions

> **NEVER assume. NEVER guess. ALWAYS ask.**

**Before creating ANY clean branch, confirm with user:**

| If unclear about... | ASK |
|---------------------|-----|
| Source branch | "Which branch contains your feature work?" |
| Clean branch name | "I'll create `{name}`. Does this look right?" |
| Base branch | "Which branch should excluded paths be restored from? (e.g., develop, main)" |
| What to exclude | "What paths should I exclude? (Default: .agent/, .github/)" |

**If ANY of these are ambiguous:**
1. Stop
2. Ask ONE question at a time
3. Wait for explicit confirmation
4. Only proceed when ALL inputs are confirmed

**NEVER:**
- Guess the base branch
- Assume exclusions without asking
- Create a branch without showing the user the exact name first
- Proceed if source branch is unclear

---

## Prerequisites

### MANDATORY: File Audit Trail

**The file-created.log MUST exist before proceeding.** This ensures we know which files to exclude.

If `.agent/log/created-files.log` does not exist:
1. **Generate it** from git history (see Generation Procedure below)
2. **Present to user** for validation
3. **Only proceed** after user confirms the list

This prevents accidental inclusion of agent-ops files in the clean branch.

---

## Invocation

User says something like:
- "Create a clean branch for PR"
- "Make a branch without .agent and .github changes"
- "Prepare my feature for code review"

---

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `source_branch` | Feature branch with work | Current branch |
| `new_branch` | Name for clean branch | `{source_branch}-clean` |
| `base_branch` | Branch to restore excluded paths from | Auto-detect |
| `exclusions` | Paths/patterns to exclude | Prompt user |

---

## Workflow

### 1. Gather Requirements

**If not provided, ask:**
1. Source branch
2. Clean branch name
3. Base branch
4. Exclusions

### 2. Validate File Audit Trail

Ensure the `.agent/log/created-files.log` exists and is validated by the user.

### 3. Create Clean Branch

Use the validated inputs to create the clean branch while excluding specified paths.