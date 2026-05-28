---
name: jira-manage
description: |
  Manage Jira tickets using jira-cli: create new issues, update existing tickets
  (summary, description, priority, labels, components), and close/transition tickets.
  Activates when user wants to: "create a ticket", "update issue", "close ticket",
  "mark as done", "change priority", or modify Jira issues.
---

# Jira Ticket Management Skill

## Purpose

Enable creation, modification, and closure of Jira tickets using the `jira` CLI
(ankitpokhrel/jira-cli). This skill handles write operations for Jira issues.

## AI Usage Note

**Always use `--plain` flag when fetching data for parsing.** The default
interactive UI is not suitable for programmatic use.

```bash
# For AI/script use
jira issue list --plain
jira issue list --plain --columns key,summary,status --no-headers

# Output formats
jira issue list --plain    # Plain text
jira issue list --csv      # CSV format
jira issue list --raw      # Raw JSON
```

## When to Use This Skill

Activate when detecting:

- **Create intent**: "create ticket", "new issue", "open a bug", "file a story"
- **Update intent**: "update ticket", "change summary", "add label", "set priority"
- **Comment intent**: "add comment", "comment on ticket", "leave a note"
- **Assign intent**: "assign ticket", "assign to me", "unassign"
- **Close intent**: "close ticket", "mark as done", "resolve issue", "transition to"
- **Link intent**: "link issues", "block ticket", "mark as duplicate"
- **Worklog intent**: "log time", "add worklog", "track time"
- **Explicit ticket IDs with modification**: "update PROJ-123", "close PROJ-456"

## Prerequisites

The `jira` CLI must be installed and configured. Assume it is properly set up
with authentication via `JIRA_API_TOKEN` environment variable.

## Command Reference

Detailed command documentation is in reference files:

- **[`references/create.md`](references/create.md)** - Creating issues and epics
- **[`references/update.md`](references/update.md)** - Editing, assigning, linking, and managing issues
- **[`references/transition.md`](references/transition.md)** - Moving issues between states
- **[`references/comment.md`](references/comment.md)** - Adding and managing comments
- **[`references/workflows.md`](references/workflows.md)** - Common workflow patterns and examples
- **[`references/scripting.md`](references/scripting.md)** - Automation and CI/CD integration

**Loading strategy:**

- Load `create.md` for new ticket requests
- Load `update.md` for modification, assignment, linking, worklog requests
- Load `transition.md` for status changes and closing tickets
- Load `comment.md` for comment operations
- Load `workflows.md` for workflow/process questions
- Load `scripting.md` for automation/CI/CD requests

## Quick Reference

### Powerful List Filters

Combine flags for precise queries:

```bash
# Personal queries
jira issue list -a$(jira me) --plain           # Assigned to me
jira issue list -r$(jira me) --plain           # Reported by me
jira issue list -w --plain                      # Issues I'm watching

# Combined filters
jira issue list -yHigh -s"In Progress" --created month -lbackend --plain

# NOT operator (~)
jira issue list -s~Done --plain                # Status NOT done
jira issue list -ax --plain                    # Unassigned
jira issue list -a~x --plain                   # Assigned to anyone

# Time-based
jira issue list --created -7d --plain          # Last 7 days
jira issue list --updated -1h --plain          # Updated in last hour
jira issue list --created week --plain         # This week
jira issue list --created-before -24w --plain  # Before 24 weeks ago

# Output control
jira issue list --plain --columns key,summary,status --no-headers
jira issue list --order-by rank --reverse --plain  # Same order as UI
```

### Create Issue

```bash
# Interactive creation
jira issue create

# Non-interactive creation (requires all parameters)
jira issue create -tBug -s"Summary text" -yHigh -b"Description" --no-input

# Create with labels and components
jira issue create -tStory -s"New feature" -lbackend -lurgent -CTeamA --no-input

# Create under an epic
jira issue create -tStory -s"New story" -PEPIC-42 --no-input
```

### Update Issue

```bash
# Interactive edit
jira issue edit PROJ-123

# Non-interactive edit
jira issue edit PROJ-123 -s"New summary" --no-input

# Add/remove labels (prefix with - to remove)
jira issue edit PROJ-123 --label newlabel --label -oldlabel --no-input

# Change priority
jira issue edit PROJ-123 -yHigh --no-input
```

### Assign Issue

```bash
# Assign to user
jira issue assign PROJ-123 "john.doe"

# Assign to self
jira issue assign PROJ-123 $(jira me)

# Unassign
jira issue assign PROJ-123 x
```

### Add Comment

```bash
# Add comment directly
jira issue comment add PROJ-123 "This is my comment"

# Add internal comment (Service Desk)
jira issue comment add PROJ-123 "Internal note" --internal

# Comment from file
jira issue comment add PROJ-123 --template /path/to/comment.md
```

### Close/Transition Issue

**Note:** The `move` command does NOT support `--no-input` or `-a` (assignee) flags.
Assignment must be done separately with `jira issue assign`.

**Note about Resolution Field:** The `-R/--resolution` flag is workflow-dependent.
Some Jira workflows don't support this field. If you get "Field 'resolution' cannot be set" error, omit the `-R` flag.

**WARNING about Comments During Transition:** The `--comment` flag often fails during transitions with "Field 'comment' cannot be set" errors. This is because many Jira workflows don't expose the comment field during state transitions. **Best practice: Always add comments separately after the transition succeeds.**

```bash
# Interactive transition (shows available states)
jira issue move PROJ-123

# Direct transition
jira issue move PROJ-123 "Done"

# RECOMMENDED: Transition first, then comment separately
jira issue move PROJ-123 Done
jira issue comment add PROJ-123 "Completed in PR #123"

# With resolution (if available in workflow)
jira issue move PROJ-123 Done -RFixed
jira issue comment add PROJ-123 "Completed in PR #123"

# Legacy: Transition with comment (may fail - not recommended)
# jira issue move PROJ-123 Done --comment "Completed in PR #123"

# IMPORTANT: State names are workflow-specific!
# Always check available transitions first:
jira issue move PROJ-123  # Lists valid transitions from current state
# Example: "In Progress" might be called "Start working" in your workflow
```

### Assign Then Transition (Common Pattern)

```bash
# Assignment cannot be done during transition - do it separately
jira issue assign PROJ-123 $(jira me)
jira issue move PROJ-123 "In Progress"
```

### Link Issues

```bash
# Create block relationship
jira issue link PROJ-123 PROJ-456 Blocks

# Link as duplicate
jira issue link PROJ-123 PROJ-456 Duplicates

# Add remote link (PR, docs)
jira issue link remote PROJ-123 "https://github.com/org/repo/pull/456" "PR #456"

# Unlink issues
jira issue unlink PROJ-123 PROJ-456
```

### Log Work

```bash
# Add worklog
jira issue worklog add PROJ-123 "2h 30m" --no-input

# Worklog with comment
jira issue worklog add PROJ-123 "1d" --comment "Implementation work" --no-input
```

### Sprint Management

```bash
# Current sprint issues
jira sprint list --current --plain

# My issues in current sprint
jira sprint list --current -a$(jira me) --plain

# Add issues to sprint
jira sprint add SPRINT_ID PROJ-123 PROJ-124
```

### Epic Management

```bash
# List issues in epic
jira epic list EPIC-42 --plain

# Add issues to epic
jira epic add EPIC-42 PROJ-123 PROJ-124

# Create epic
jira epic create -n"Epic Name" -s"Epic Summary" -yHigh --no-input
```

### Clone Issue

```bash
# Simple clone
jira issue clone PROJ-123

# Clone with modifications
jira issue clone PROJ-123 -s"[Clone] Original summary" -yMedium -a$(jira me)

# Clone with text replacement
jira issue clone PROJ-123 -H"production:staging"
```

### Delete Issue

```bash
# Delete issue
jira issue delete PROJ-123

# Delete with subtasks
jira issue delete PROJ-123 --cascade
```

## Interactive UI Navigation

When using interactive mode (without `--plain`):

| Key             | Action                |
| --------------- | --------------------- |
| `j/k` or arrows | Navigate up/down      |
| `g/G`           | Jump to top/bottom    |
| `v`             | View issue details    |
| `m`             | Transition issue      |
| `Enter`         | Open in browser       |
| `c`             | Copy URL to clipboard |
| `Ctrl+k`        | Copy issue key        |
| `Ctrl+r` / `F5` | Refresh               |
| `q` / `Esc`     | Quit                  |
| `?`             | Help                  |

## Workflow Guidelines

### Creating Tickets

1. **Gather required information** before creating:
   - Type (Bug, Story, Task, Epic)
   - Summary (required)
   - Priority (optional but recommended)
   - Description (optional)
   - Labels/Components (optional)

2. **Confirm with user** before execution:

   ```
   I'll create the following ticket:
   - Type: Bug
   - Summary: Login fails with special characters
   - Priority: High
   - Labels: auth, urgent

   Proceed? [y/N]
   ```

3. **Report the created ticket key** after success

### Updating Tickets

1. **Show current state** before modifying (use `jira issue view PROJ-123`)
2. **Confirm changes** with user before applying
3. **Use `--no-input`** for non-interactive updates
4. **Handle label/component removal** with `-` prefix

### Closing Tickets

1. **Check available transitions** if needed:

   ```bash
   jira issue move PROJ-123  # Shows available transitions interactively
   ```

2. **Try to include resolution** when closing (if supported by workflow). Common resolutions: Fixed, Won't Fix, Duplicate. If you encounter "Field 'resolution' cannot be set" error, omit the `-R` flag.

3. **Add closing comments separately** after transition succeeds:

   ```bash
   # First transition
   jira issue move PROJ-123 Done -RFixed
   # Then add comment
   jira issue comment add PROJ-123 "Completed in PR #123"
   ```

   This two-step approach avoids "Field 'comment' cannot be set" errors that commonly occur when using `--comment` flag during transitions.

## Error Handling

### Common Errors

**Invalid issue type:**

```
Error: issue type "X" is not valid
```

Recovery: List available types with `jira project list` and use correct type name.

**Invalid transition:**

```
Error: transition "X" is not valid
```

Recovery: The issue's current state may not allow that transition. Check workflow.

**Missing required fields:**

```
Error: required field "X" is missing
```

Recovery: Prompt user for the missing field value.

### Authentication Issues

If commands fail with authentication errors:

```
Jira CLI authentication may have expired. Please run:
jira init
```

## Security Considerations

- **Always confirm** before executing write operations
- **Never commit** sensitive data in descriptions or comments
- **Validate input** before passing to CLI commands
- **Quote all user-provided strings** to prevent injection

## Response Formatting

After successful operations, report:

**Created:**

```
Created PROJ-123: Login fails with special characters
Type: Bug | Priority: High | Status: To Do
URL: https://yourinstance.atlassian.net/browse/PROJ-123
```

**Updated:**

```
Updated PROJ-123:
- Summary: "Old summary" -> "New summary"
- Priority: Medium -> High
- Labels: +urgent, -backlog
```

**Assigned:**

```
PROJ-123 assigned to john.doe
```

**Commented:**

```
Comment added to PROJ-123
```

**Transitioned:**

```
PROJ-123 moved to Done
Resolution: Fixed (if set)
```

If comment was needed, add separately:

```
Comment added: "Completed in PR #123"
```

**Linked:**

```
PROJ-123 now blocks PROJ-456
```

**Worklog:**

```
Logged 2h 30m on PROJ-123
```

## Resources

- **GitHub**: <https://github.com/ankitpokhrel/jira-cli>
- **Installation**: <https://github.com/ankitpokhrel/jira-cli/wiki/Installation>
- **FAQs**: <https://github.com/ankitpokhrel/jira-cli/discussions/categories/faqs>
