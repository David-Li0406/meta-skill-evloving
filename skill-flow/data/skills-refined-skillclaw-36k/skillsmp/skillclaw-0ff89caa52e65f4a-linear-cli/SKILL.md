---
name: linear-cli
description: Use this skill to manage Linear issues and projects from the command line, automating your Linear project management tasks.
---

# Linear CLI

A cross-platform CLI for managing Linear issues and projects using Linear's GraphQL API.

## Prerequisites

Ensure the `linear` command is available on your PATH. To check:

```bash
linear --version
```

If not installed, follow the instructions at:\
https://github.com/schpet/linear-cli?tab=readme-ov-file#install

## First-Time Setup

Run the following command to log in and set up your configuration:

```bash
linear login
```

This will:
1. Ask where to save credentials (project or global).
2. Open Linear API settings in your browser.
3. Prompt you to paste your API key.
4. Show available teams and let you pick one (or create a new team).
5. Save the configuration to the chosen location.

## Configuration

Config is loaded in order: `./.linear` → `~/.linear` → environment variables.

Example `.linear` file format:

```
api_key=lin_api_xxx
team=ISSUE
```

## Available Commands

### Authentication
```bash
linear login                    # Interactive setup
linear logout                   # Remove config
linear whoami                   # Show current user/team
```

### Issues
```bash
linear issues --unblocked       # Ready to work on (no blockers)
linear issues --open            # All non-completed issues
linear issues --backlog         # Backlog issues only
linear issues --in-progress     # Issues currently in progress
linear issues --mine            # Only your assigned issues
linear issues --project "Name"  # Issues in a project
linear issues --milestone "M1"  # Issues in a milestone
linear issues --label bug       # Filter by label
linear issue show ISSUE-1       # Full details with parent context
linear issue start ISSUE-1      # Assign to you + set In Progress
linear issue create --title "Fix bug" --project "Phase 1" --assign --estimate M
linear issue update ISSUE-1 --state "In Progress"
linear issue close ISSUE-1
linear issue comment ISSUE-1 "Comment text"
```

### Projects
```bash
linear projects                 # Active projects
linear project show "Phase 1"   # Details with issues
linear project create "Name" --description "..."
linear project complete "Phase 1"
```

### Milestones
```bash
linear milestone                # Manage Linear project milestones
```

## Discovering Options

To see available subcommands and flags, run `--help` on any command:

```bash
linear --help
linear issue --help
linear project --help
```