---
name: linear-cli
description: Use this skill to manage Linear issues and projects from the command line, automating project management tasks effectively.
---

# Linear CLI

A cross-platform CLI to manage Linear issues and projects using Linear's GraphQL API.

## Prerequisites

Ensure the `linear` command is available on your PATH. Check with:

```bash
linear --version
```

If not installed, follow the instructions at:\
[Linear CLI Installation](https://github.com/schpet/linear-cli?tab=readme-ov-file#install)

## First-Time Setup

Run the following command to log in and set up your environment:

```bash
linear login
```

This will prompt you to save credentials, open Linear API settings in your browser, and allow you to select a team.

## Available Commands

### Authentication
```bash
linear auth               # Manage Linear authentication
linear login              # Interactive setup
linear logout             # Remove config
linear whoami             # Show current user/team
```

### Issues Management
```bash
linear issue              # Manage Linear issues
linear issues --open      # All non-completed issues
linear issues --mine      # Only your assigned issues
linear issue create --title "<title>" --project "<project>" --assign --estimate <size>
linear issue update <issue_id> --state "<state>"
linear issue close <issue_id>
linear issue comment <issue_id> "<comment>"
```

### Project Management
```bash
linear project            # Manage Linear projects
linear projects           # List active projects
linear project create "<name>" --description "<description>"
linear project complete "<name>"
```

### Milestones Management
```bash
linear milestone          # Manage Linear project milestones
linear milestones --project "<project>" # List milestones in a project
linear milestone create "<name>" --project "<project>" --target-date <date>
```

### Labels Management
```bash
linear label              # Manage Linear issue labels
linear labels             # List all labels
linear label create "<name>" --color "<color>"
```

## Workflow Guidelines

### Getting Oriented
To see all projects and their progress, use:

```bash
linear roadmap
```

### Starting Work on an Issue
Find unblocked issues and start working:

```bash
linear issues --unblocked
linear issue start <issue_id>
```

### Handling Blockers
If you encounter a blocker, create a blocking issue:

```bash
linear issue create --title "<title>" --blocks <blocking_issue_id>
```

### Completing Work
After finishing implementation, suggest closing the issue:

```bash
linear issue close <issue_id>
```

### Adding Notes
To add notes while working on an issue:

```bash
linear issue update <issue_id> --append "<notes>"
```

### Organizing with Milestones
Create and manage milestones to group related issues:

```bash
linear milestone create "<name>" --project "<project>" --target-date <date>
```

## Estimation
Use t-shirt sizes for estimates:

| Size | Meaning |
|------|---------|
| XS   | Trivial, < 1 hour |
| S    | Small, couple hours |
| M    | Medium, a day or so |
| L    | Large, multi-day |
| XL   | Very large |

## Git Conventions
Link git work to Linear issues:

```bash
linear branch <issue_id>            # Create branch from issue
git commit -m "<issue_id>: <message>" # Commit message format
```

## Discovering Options
To see available subcommands and flags, run:

```bash
linear --help
linear issue --help
```

For detailed help on any command, append `--help`.