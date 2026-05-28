---
name: linear-cli
description: Manage Linear issues and projects from the command line. This skill allows automating Linear project management.
allowed-tools: Bash(linear:*), Bash(curl:*)
---

# Linear CLI

A cross-platform CLI for Linear's GraphQL API, with unblocked issue filtering.

Install: `npm install -g @dabble/linear-cli`

## First-Time Setup

```bash
linear login
```

This will:
1. Ask where to save credentials (project or global)
2. Open Linear API settings in your browser
3. Prompt you to paste your API key
4. Show available teams and let you pick one (or create a new team)
5. Save config to the chosen location

## Configuration

Config is loaded in order: `./.linear` → `~/.linear` → env vars

```
# .linear file format
api_key=lin_api_xxx
team=ISSUE
```

## Quick Reference

```bash
# Auth
linear login                    # Interactive setup
linear logout                   # Remove config
linear whoami                   # Show current user/team

# Roadmap (overview)
linear roadmap                  # Projects with milestones and progress

# Issues
linear issues --unblocked       # Ready to work on (no blockers)
linear issues --open            # All non-completed issues
linear issues --backlog         # Backlog issues only
linear issues --in-progress     # Issues currently in progress
linear issues --mine            # Only your assigned issues
linear issues --project "Name"  # Issues in a project
linear issues --milestone "M1"  # Issues in a milestone
linear issues --label bug       # Filter by label
# Flags can be combined: linear issues --in-progress --mine
linear issue show ISSUE-1        # Full details with parent context
linear issue start ISSUE-1       # Assign to you + set In Progress
linear issue create --title "Fix bug" --project "Phase 1" --assign --estimate M
linear issue create --title "Task" --milestone "Beta" --estimate S
linear issue create --title "Blocked task" --blocked-by ISSUE-1
linear issue update ISSUE-1 --state "In Progress"
linear issue update ISSUE-1 --milestone "Beta"
linear issue update ISSUE-1 --append "Notes..."
linear issue update ISSUE-1 --blocks ISSUE-2  # Add blocking relation
linear issue close ISSUE-1
linear issue comment ISSUE-1 "Comment text"

# Projects
linear projects                 # Active projects
linear projects --all           # Include completed
linear project show "Phase 1"   # Details with issues
linear project create "Name" --description "..."
linear project complete "Phase 1"

# Milestones
linear milestones --project "P1" # Milestones in a project
linear milestone show "Beta"     # Details with issues
linear milestone create "Beta" --project "P1" --target-date 2024-03-01

# Reordering (drag-drop equivalent)
linear projects reorder "P1" "P2" "P3"           # Set project order
linear project move "Urgent" --before "Phase 1"  # Move single project
linear milestones reorder "Alpha" "Beta" --project "P1"
linear milestone move "Beta" --after "Alpha" --project "P1"
linear issues reorder ISSUE-1 ISSUE-2 ISSUE-3    # Set issue order
linear issue move ISSUE-5 --before ISSUE-1       # Move single issue

# Labels
linear labels                   # List all labels
linear label create "bug" --color "#FF0000"

# Git
linear branch ISSUE-1            # Create branch: ISSUE-1-issue-title
```

## Estimation

Use t-shirt sizes for estimates. Always use `--estimate` (not `-e`) for clarity.

| Size | Meaning |
|------|---------|
| XS | Trivial, < 1 hour |
| S | Small, couple hours |
| M | Medium, a day or so |
| L | Large, multi-day - consider breaking down |
| XL | Very large - should definitely break down |

```bash
# Create with estimate (use long flags for clarity)
linear issue create --title "Add caching" --estimate M --assign

# L/XL issues should be broken into sub-issues
linear issue create --title "Implement auth" --estimate L
linear issue create --title "Add login endpoint" --parent ISSUE-5 --estimate S
linear issue create --title "Add JWT validation" --parent ISSUE-5 --estimate S
```

## Git Conventions

Always link git work to Linear issues:

```bash
# Create branch from issue (recommended)
linear branch ISSUE-5            # Creates: ISSUE-5-add-caching-layer

# Commit message format
git commit -m "ISSUE-5: Add cache invalidation on logout"

# Include issue ID in PR title
gh pr create --title "ISSUE-5: Add caching layer"
```

## Workflow Guidelines

### Getting oriented
```bash
linear roadmap                  # See all projects, milestones, progress
linear issues --project "P1"    # Issues in a specific project
linear issues --milestone "M1"  # Issues in a specific milestone
```

### Starting work on an issue
```bash
linear issues --unblocked       # Find what's ready
linear issue show ISSUE-2        # Review it (shows parent context)
linear issue start ISSUE-2       # Assign + set In Progress
linear branch ISSUE-2            # Create git branch
```

### When you hit a blocker
If work cannot continue due to a dependency or external factor:

```bash
# Create the blocking issue
linear issue create --title "Need API credentials" --blocks ISSUE-5

# Or mark existing issue as blocking
linear issue update ISSUE-3 --blocks ISSUE-5
```

This removes ISSUE-5 from `--unblocked` results until the blocker is resolved.

### When a task is larger than expected
If you discover an M issue is actually L/XL, break it down:

```bash
# Create sub-issues
linear issue create --title "Step 1: Research approach" --parent ISSUE-5 --estimate S
linear issue create --title "Step 2: Implement core logic" --parent ISSUE-5 --estimate M
linear issue create --title "Step 3: Add tests" --parent ISSUE-5 --estimate S

# Start working on the first sub-issue
linear issue start ISSUE-6
```

### Completing work
After finishing implementation, ask the developer if they want to close the issue:

```bash
# Suggest closing
linear issue close ISSUE-5
```

Do not auto-close issues. Let the developer review the work first.

### Adding notes while working
```bash
linear issue update ISSUE-2 --append "## Notes\n\nDiscovered X, trying Y approach..."
# or for quick updates
linear issue comment ISSUE-2 "Found the root cause in auth.ts:142"
```

### Organizing with milestones
Milestones group related issues within a project:

```bash
# Create milestone for a release
linear milestone create "Beta" --project "Phase 1" --target-date 2024-03-01

# Add issues to milestone
linear issue create --title "Core feature" --milestone "Beta" --estimate M
linear issue update ISSUE-5 --milestone "Beta"

# Reorder milestones to reflect priority
linear milestones reorder "Alpha" "Beta" "Stable" --project "Phase 1"
```

### Completing a phase
```bash
linear issue close ISSUE-7       # Close remaining issues
linear project complete "Phase 1"
# Then update CLAUDE.md status table
```

## Parent Context

When viewing an issue with `linear issue show`, you'll see where it fits in the larger work:

```
# ISSUE-6: Add JWT validation

State: In Progress
...

## Context

ISSUE-3: Implement authentication system
  - [Done] ISSUE-4: Add login endpoint
  → [In Progress] ISSUE-6: Add JWT validation  ← you are here
  - [Backlog] ISSUE-7: Add refresh tokens
```

This helps understand the scope and what comes before/after the current task.
