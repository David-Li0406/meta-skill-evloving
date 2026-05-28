# Transition Issue Commands

Reference for moving Jira issues between workflow states using `jira-cli`.

## Getting Help

```bash
jira issue move --help
```

## Move/Transition Issue

```bash
jira issue move [ISSUE-KEY] [STATE]
```

### Options

| Flag                            | Description                                                      |
| ------------------------------- | ---------------------------------------------------------------- |
| `-R, --resolution <resolution>` | Set resolution (optional, workflow-dependent)                    |
| `--comment <text>`              | Add comment during transition (WARNING: often fails - see below) |

**Note:** The `move` command does NOT support:

- `--no-input` flag - transitions are always direct when state is provided
- `-a, --assignee` flag - assignment during transition often fails with "Field 'assignee' cannot be set"

Use `jira issue assign` separately for assignment.

**Note about Resolution Field:**

- The `-R/--resolution` flag is workflow and screen configuration dependent
- Some Jira workflows/projects don't support the resolution field
- If you get "Field 'resolution' cannot be set" error, omit the `-R` flag

**WARNING about --comment Flag:**
The `--comment` flag frequently fails with "Field 'comment' cannot be set" errors because many Jira workflows don't expose the comment field during state transitions. This is a screen configuration issue in Jira, not a CLI bug.

**BEST PRACTICE:** Always add comments as a separate step after the transition succeeds:

```bash
# Recommended approach
jira issue move PROJ-123 Done -RFixed
jira issue comment add PROJ-123 "Completed in PR #123"

# Not recommended (will often fail)
# jira issue move PROJ-123 Done -RFixed --comment "Completed in PR #123"
```

### Examples

```bash
# Interactive transition (shows available states)
jira issue move
jira issue move PROJ-123

# Move to specific state
jira issue move PROJ-123 "In Progress"
jira issue move PROJ-123 "Done"
jira issue move PROJ-123 "To Do"

# Close with resolution (if available in workflow)
jira issue move PROJ-123 Done -RFixed
jira issue move PROJ-123 Done -R"Won't Fix"
jira issue move PROJ-123 Done -RDuplicate

# Close without resolution (for workflows that don't support it)
jira issue move PROJ-123 Done

# RECOMMENDED: Transition then comment separately
jira issue move PROJ-123 "In Progress"
jira issue comment add PROJ-123 "Starting work on this"

jira issue move PROJ-123 Done -RFixed
jira issue comment add PROJ-123 "Completed in PR #456"

# Legacy: Transition with comment (may fail - not recommended unless workflow supports it)
# jira issue move PROJ-123 "In Progress" --comment "Starting work on this"
# jira issue move PROJ-123 Done --comment "Completed in PR #456"
```

### Assignment During Transition

**IMPORTANT:** The `-a/--assignee` flag often fails with:

```
Error: Field 'assignee' cannot be set. It is not on the appropriate screen, or unknown.
```

Instead, assign separately:

```bash
# Assign first, then transition
jira issue assign PROJ-123 $(jira me)
jira issue move PROJ-123 "In Progress"
```

## Common Resolutions

**NOTE:** Resolution field availability varies by Jira instance and workflow configuration.
If the resolution field is not available in your workflow, simply omit the `-R` flag.

When closing issues with resolution support, use appropriate resolutions:

| Resolution         | When to Use                        |
| ------------------ | ---------------------------------- |
| `Fixed`            | Issue was resolved as intended     |
| `Won't Fix`        | Issue won't be addressed           |
| `Duplicate`        | Issue duplicates another           |
| `Cannot Reproduce` | Unable to replicate the issue      |
| `Done`             | Work completed (for stories/tasks) |
| `Incomplete`       | Closed without full completion     |

## Common Workflow States

Standard Jira workflow states (may vary by project):

| State         | Description               |
| ------------- | ------------------------- |
| `To Do`       | Not started               |
| `In Progress` | Currently being worked on |
| `In Review`   | Under review/QA           |
| `Done`        | Completed                 |
| `Blocked`     | Cannot proceed            |
| `On Hold`     | Temporarily paused        |

**IMPORTANT:** State names and transition names are project/workflow-specific!

Common variations:

- `To Do` / `Open` / `New` / `Backlog`
- `In Progress` / `Active` / `In Development` / `Start working` (transition name)
- `Done` / `Closed` / `Resolved` / `Complete`
- `Refined` (common intermediate state before "In Progress")

**Always check available transitions first:**

```bash
jira issue move PROJ-123
# Shows: Available states for issue PROJ-123: 'Blocked', 'Start working', 'Refined', etc.
```

## Workflow Considerations

### Valid Transitions

Not all transitions are valid from every state. The workflow defines allowed paths:

```
To Do -> In Progress -> In Review -> Done
           |              |
           v              v
        Blocked      On Hold
```

If a transition fails, check available transitions interactively:

```bash
jira issue move PROJ-123
# Shows list of valid transitions from current state
```

### State Names Are Project-Specific

State names and **transition names** can vary by project. Common variations:

- `To Do` / `Open` / `New` / `Backlog`
- `In Progress` / `Active` / `In Development`
- `Done` / `Closed` / `Resolved` / `Complete`

**Transition names may differ from state names!**
For example, to reach "In Progress" state, the transition might be called "Start working".

Always use the exact transition name shown by `jira issue move PROJ-123`.

## Patterns for Common Actions

### Start Working on Issue

```bash
# Assign to self first (cannot combine with move)
jira issue assign PROJ-123 $(jira me)
jira issue move PROJ-123 "In Progress"
jira issue comment add PROJ-123 "Starting work"
# Note: transition name might be "Start working" - check with: jira issue move PROJ-123
```

### Complete Issue

```bash
# Mark as done with resolution (if available)
jira issue move PROJ-123 Done -RFixed
jira issue comment add PROJ-123 "Completed"

# Or without resolution (for workflows without this field)
jira issue move PROJ-123 Done
jira issue comment add PROJ-123 "Completed"
```

### Close as Won't Fix

```bash
# With resolution (if available in workflow)
jira issue move PROJ-123 Done -R"Won't Fix"
jira issue comment add PROJ-123 "Out of scope for this release"

# Without resolution
jira issue move PROJ-123 Done
jira issue comment add PROJ-123 "Won't Fix: Out of scope for this release"
```

### Close as Duplicate

```bash
# First link to original
jira issue link PROJ-123 PROJ-100 Duplicates

# Then close with resolution (if available)
jira issue move PROJ-123 Done -RDuplicate
jira issue comment add PROJ-123 "Duplicate of PROJ-100"

# Or without resolution
jira issue move PROJ-123 Done
jira issue comment add PROJ-123 "Duplicate of PROJ-100"
```

### Block Issue

```bash
jira issue move PROJ-123 Blocked
jira issue comment add PROJ-123 "Waiting on external API access"
```

### Reopen Issue

```bash
jira issue move PROJ-123 "To Do"
jira issue comment add PROJ-123 "Reopening - fix incomplete"
```

### Send for Review

```bash
jira issue move PROJ-123 "In Review"
jira issue comment add PROJ-123 "Ready for code review"
```

## Error Handling

### Invalid Transition

```
Error: transition "Done" is not valid for issue PROJ-123
```

**Cause:** The workflow doesn't allow direct transition from current state to target.

**Solution:** Check current state and available transitions:

```bash
jira issue view PROJ-123  # Check current status
jira issue move PROJ-123  # See available transitions
```

### Missing Resolution

```
Error: resolution is required for this transition
```

**Cause:** Closing transitions often require a resolution.

**Solution:** Add resolution flag:

```bash
jira issue move PROJ-123 Done -RFixed
```

### Resolution Field Cannot Be Set

```
Error: Field 'resolution' cannot be set. It is not on the appropriate screen, or unknown.
```

**Cause:** The resolution field is not available in this workflow/screen configuration.

**Solution:** Omit the `-R/--resolution` flag and transition without it:

```bash
# Instead of:
jira issue move PROJ-123 Done -RFixed --comment "Completed"

# Use:
jira issue move PROJ-123 Done
jira issue comment add PROJ-123 "Completed"
```

### Comment Field Cannot Be Set

```
Error: Field 'comment' cannot be set. It is not on the appropriate screen, or unknown.
```

**Cause:** The comment field is not available during this transition's screen configuration. This is very common in Jira workflows where the transition screen doesn't include a comment field.

**Solution:** Always add comments as a separate step after the transition:

```bash
# Instead of:
jira issue move PROJ-123 Done --comment "Completed"

# Use:
jira issue move PROJ-123 Done
jira issue comment add PROJ-123 "Completed"
```

This two-step approach works reliably across all Jira workflows.

### Invalid Resolution

```
Error: resolution "X" is not valid
```

**Cause:** The specified resolution doesn't exist in the project.

**Solution:** Use a standard resolution like `Fixed`, `Won't Fix`, `Duplicate`.

## Best Practices

1. **Include resolution when available** - Try using `-R` flag when closing; if you get "Field cannot be set" error, omit it
2. **Add comments separately after transition** - Use `jira issue comment add` after `jira issue move` to avoid "Field 'comment' cannot be set" errors
3. **Check available transitions** before assuming a path
4. **Assign separately** - Use `jira issue assign` before or after transition, not during
5. **Link duplicates** before closing as duplicate
6. **Confirm with user** before executing transitions

## Scripting Patterns

### Close Multiple Issues

```bash
for issue in PROJ-123 PROJ-124 PROJ-125; do
  jira issue move "$issue" Done -RFixed --comment "Bulk close: Sprint cleanup"
done
```

### Transition Pipeline

```bash
# Development workflow
jira issue assign PROJ-123 $(jira me)
jira issue move PROJ-123 "In Progress"
# ... do work ...
jira issue move PROJ-123 "In Review"
jira issue comment add PROJ-123 "PR #456 ready for review"
# ... after review ...
jira issue move PROJ-123 Done -RFixed
jira issue comment add PROJ-123 "Merged"
```
