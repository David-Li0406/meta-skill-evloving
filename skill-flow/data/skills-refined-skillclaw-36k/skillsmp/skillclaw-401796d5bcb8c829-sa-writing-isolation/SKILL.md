---
name: sa-writing-isolation
description: Use this skill when you need to create an isolated writing workspace for drafting new chapters or modifying arguments, ensuring a structured and secure writing process.
---

# Skill body

## Overview

This skill allows you to create an isolated workspace for drafting chapters, ensuring that your writing process is organized and free from distractions. It combines the principles of argument-driven writing with the creation of a secure draft branch.

## Steps to Use the Skill

### 1. Declare Your Intent

Start by stating: “I am using the sa-writing-isolation skill to set up an isolated writing workspace.”

### 2. Select the Draft Directory

Follow this priority order to check for existing directories:

```bash
# Check for existing directories
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative
```

- **If found:** Use that directory. If both exist, prefer `.worktrees`.

### 3. Check for Preferences in CLAUDE.md

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

- **If specified:** Use the preferred directory directly.

### 4. Ask the Researcher

If no directory exists and no preference is found:

```
No draft directory found. Where should I create the draft branch?

1. .worktrees/ (local to the project, hidden)
2. ~/.config/superpowers/worktrees/<project-name>/ (global location)

Which do you prefer?
```

### 5. Validate Directory for Security

#### For Local Directories (.worktrees or worktrees)

**Verify that the directory is not ignored:**

```bash
# Check if the directory is ignored
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

- **If not ignored:** Follow the "immediate fix" rule:
  1. Add the relevant line to .gitignore
  2. Commit the changes
  3. Proceed to create the worktree

### 6. Create the Worktree

#### Detect Project Name

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

#### Create the Worktree

```bash
# Determine full path
case $LOCATION in
  .worktrees|worktrees)
    path="$LOCATION/$BRANCH_NAME"
    ;;
  ~/.config/superpowers/worktrees/*)
    path="~/.config/superpowers/worktrees/$project/$BRANCH_NAME"
    ;;
esac

# Create the worktree with the new branch
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

### 7. Run Project Setup

Automatically detect and run the appropriate setup for your writing environment (e.g., LaTeX or Markdown):

```bash
# LaTeX project
if [ -f main.tex ]; then echo "LaTeX project detected"; fi

# Markdown/Pandoc project
if [ -f Makefile ]; then make setup; fi
```

### 8. Verify Clean Baseline

Run a verification script to ensure the draft starts from a clean state:

```bash
# Example
make verify
# or
./scripts/validate_structure.sh
```

- **If verification fails:** Report the failure and ask whether to continue or investigate.
- **If verification passes:** Report readiness.

### 9. Report Location

```
Draft workspace ready at <full-path>
Baseline check passed
Ready to write <chapter-name>
```

## Key Principles

- **One Question at a Time:** Avoid overwhelming the researcher with multiple questions.
- **Incremental Validation:** Present the outline in segments and validate each part.
- **Flexibility:** Be prepared to clarify and adjust if certain content does not make sense.

## Common Errors

- **Skipping Validation:** Always validate that the draft directory is ignored to prevent contamination of the git status.
- **Assuming Directory Locations:** Follow the priority order for directory selection to maintain consistency.
- **Continuing After Verification Failure:** Always report failures and seek explicit permission to proceed.

## Example Workflow

```
You: I am using the sa-writing-isolation skill to set up an isolated writing workspace.

[Check .worktrees/ - exists]
[Validate ignored - git check-ignore confirms .worktrees/ is not tracked]
```