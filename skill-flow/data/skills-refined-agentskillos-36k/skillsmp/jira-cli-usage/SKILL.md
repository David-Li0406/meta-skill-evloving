---
name: Jira CLI Usage
description: This skill should be used when the user asks to "interact with Jira", "list Jira issues", "create Jira issue", "manage sprints", "view epics", "search issues", "move issue status", "assign issue", or mentions using the jira command-line tool for project management.
version: 0.1.0
---

## Purpose

Use the Jira CLI (`jira`) to interact with Jira issues, sprints, epics, and projects directly from the command line. This enables fast issue management without leaving the terminal.

## Prerequisites

- Jira CLI installed (`jira` command available)
- Configured with `jira init` (API token set via `JIRA_API_TOKEN` environment variable)

## Critical: Non-Interactive Mode Required

**NEVER use interactive mode.** Always use one of these flags:

- `--plain` - Use for standard output (default choice)
- `--raw` - Use when detailed/structured JSON data is needed for parsing

Interactive mode requires user input and will hang. Always append `--plain` or `--raw` to commands.

## Quick Reference

### Core Commands

| Command | Description |
|---------|-------------|
| `jira issue list --plain` | List recent issues in the project |
| `jira issue create -tTask -s"Summary" --no-input` | Create a new issue non-interactively |
| `jira issue view ISSUE-123 --plain` | View issue details |
| `jira issue view ISSUE-123 --raw` | View issue details as JSON |
| `jira issue edit ISSUE-123 -s"Title"` | Edit an issue |
| `jira issue move ISSUE-123 "Done"` | Transition issue status |
| `jira issue assign ISSUE-123 username` | Assign issue to user |
| `jira sprint list --current --plain` | View current sprint |
| `jira epic list --plain` | List epics in project |
| `jira open ISSUE-123` | Open issue in browser |

### Configuration

```bash
# View current user
jira me

# Server information
jira serverinfo

# Use specific project
jira issue list -p PROJECT_KEY

```

## Workflow Instructions

### Listing Issues

List issues with various filters (always use `--plain` or `--raw`):

```bash
# List all recent issues
jira issue list --plain

# Filter by assignee (current user)
jira issue list -a$(jira me) --plain

# Filter by status
jira issue list -s"In Progress" --plain

# Filter by priority
jira issue list -yHigh --plain

# Filter by creation date
jira issue list --created month --plain

# Combine filters
jira issue list -a$(jira me) -yHigh -s"To Do" --created month --plain

# JSON output when detailed data needed
jira issue list --raw
```

### Creating Issues

Always provide required fields to avoid interactive prompts:

```bash
# Create with required fields (use --no-input to prevent prompts)
jira issue create -t"Bug" -s"Fix login error" -b"Description here" --no-input

# Create and assign
jira issue create -t"Task" -s"New feature" -a$(jira me) --no-input

# Create with priority
jira issue create -t"Task" -s"Urgent fix" -yHigh --no-input
```

### Viewing and Editing Issues

```bash
# View full issue details (plain text)
jira issue view ISSUE-123 --plain

# View full issue details (JSON for parsing)
jira issue view ISSUE-123 --raw

# Edit issue summary
jira issue edit ISSUE-123 -s"Updated title" --no-input

# Edit issue body/description
jira issue edit ISSUE-123 -b"Updated description" --no-input

# Add comment
jira issue comment add ISSUE-123 -b"Comment text" --no-input
```

### Moving Issues Through Workflow

Always specify the target status explicitly:

```bash
# Move to specific status
jira issue move ISSUE-123 "In Progress"
jira issue move ISSUE-123 "Done"
jira issue move ISSUE-123 "To Do"
```

### Sprint Management

```bash
# List all sprints
jira sprint list --plain

# View current sprint
jira sprint list --current --plain

# View sprint issues
jira sprint list SPRINT_ID --plain

# Filter sprint issues by assignee
jira sprint list SPRINT_ID -a me --plain

# Get sprint data as JSON
jira sprint list --current --raw
```

### Epic Management

```bash
# List epics
jira epic list --plain

# View epic issues
jira epic list EPIC-123 --plain

# Add issue to epic
jira epic add EPIC-123 ISSUE-456
```

### Board Operations

```bash
# List boards
jira board list --plain

# View board details
jira board view BOARD_ID --plain
```

## Output Formats

Always use non-interactive output:

- **Plain text** (`--plain`): Default choice for readable output
- **JSON** (`--raw`): Use when detailed/structured data is needed for parsing
- **CSV** (`--csv`): Use for spreadsheet export

**Never use interactive mode** - it requires user input and will hang.

## Common Patterns

### Daily Standup Check

```bash
# See what you're working on
jira issue list -a$(jira me) -s"In Progress" --plain

# Check current sprint
jira sprint list --current --plain
```

### Start Working on Issue

```bash
# View issue details
jira issue view ISSUE-123 --plain

# Assign to yourself and move to In Progress
jira issue assign ISSUE-123 $(jira me)
jira issue move ISSUE-123 "In Progress"
```

### Complete an Issue

```bash
# Move to done
jira issue move ISSUE-123 "Done"

# Add completion comment
jira issue comment add ISSUE-123 -b"Completed and deployed" --no-input
```

## Troubleshooting

### Check Configuration

```bash
# Verify current user
jira me

# Check server connection
jira serverinfo

# Debug mode
jira --debug issue list --plain
```

### Common Issues

- **Authentication errors**: Ensure `JIRA_API_TOKEN` is set correctly
- **Project not found**: Use `-p PROJECT_KEY` to specify project
- **Invalid transition**: Check issue status first with `jira issue view ISSUE-123 --plain` to see available transitions
