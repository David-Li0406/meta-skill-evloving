# Update Issue Commands

Reference for editing and modifying Jira issues using `jira-cli`.

## Getting Help

```bash
jira issue edit --help
jira issue assign --help
jira issue link --help
jira issue worklog add --help
```

## Edit Issue

```bash
jira issue edit <ISSUE-KEY> [options]
```

### Options

| Flag                        | Description                                 |
| --------------------------- | ------------------------------------------- |
| `-s, --summary <text>`      | New summary/title                           |
| `-b, --body <text>`         | New description                             |
| `-y, --priority <priority>` | New priority                                |
| `-a, --assignee <user>`     | New assignee                                |
| `-l, --label <label>`       | Add label (prefix with `-` to remove)       |
| `-C, --component <name>`    | Add component (prefix with `-` to remove)   |
| `--fix-version <version>`   | Add fix version (prefix with `-` to remove) |
| `--no-input`                | Disable interactive prompts                 |

### Examples

```bash
# Interactive edit (opens editor for all fields)
jira issue edit PROJ-123

# Update summary only
jira issue edit PROJ-123 -s"Updated summary text" --no-input

# Update priority
jira issue edit PROJ-123 -yHigh --no-input

# Update description
jira issue edit PROJ-123 -b"New description content" --no-input

# Multiple updates at once
jira issue edit PROJ-123 \
  -s"New summary" \
  -yHigh \
  -b"Updated description" \
  --no-input
```

### Managing Labels

Labels support add and remove in a single command:

```bash
# Add labels
jira issue edit PROJ-123 --label bug --label urgent --no-input

# Remove labels (prefix with -)
jira issue edit PROJ-123 --label -backlog --label -low-priority --no-input

# Add and remove in same command
jira issue edit PROJ-123 \
  --label -p2 \
  --label p1 \
  --label -needs-triage \
  --label reviewed \
  --no-input
```

### Managing Components

Components work the same as labels:

```bash
# Add component
jira issue edit PROJ-123 --component Backend --no-input

# Remove component
jira issue edit PROJ-123 --component -Frontend --no-input

# Add and remove
jira issue edit PROJ-123 \
  --component -OldTeam \
  --component NewTeam \
  --no-input
```

### Managing Fix Versions

```bash
# Add fix version
jira issue edit PROJ-123 --fix-version v2.0 --no-input

# Remove fix version
jira issue edit PROJ-123 --fix-version -v1.0 --no-input

# Change fix version
jira issue edit PROJ-123 \
  --fix-version -v1.0 \
  --fix-version v2.0 \
  --no-input
```

## Assign Issue

```bash
jira issue assign [ISSUE-KEY] [ASSIGNEE]
```

### Examples

```bash
# Interactive assignment
jira issue assign
jira issue assign PROJ-123

# Assign to specific user
jira issue assign PROJ-123 "john.doe"

# Assign to yourself
jira issue assign PROJ-123 $(jira me)

# Assign to default assignee
jira issue assign PROJ-123 default

# Unassign (remove assignee)
jira issue assign PROJ-123 x
```

## Link Issues

```bash
jira issue link <SOURCE-KEY> <TARGET-KEY> <LINK-TYPE>
```

### Common Link Types

| Link Type          | Description                    |
| ------------------ | ------------------------------ |
| `Blocks`           | Source blocks target           |
| `is blocked by`    | Source is blocked by target    |
| `Clones`           | Source clones target           |
| `is cloned by`     | Source is cloned by target     |
| `Duplicates`       | Source duplicates target       |
| `is duplicated by` | Source is duplicated by target |
| `Relates to`       | General relationship           |

### Examples

```bash
# Interactive linking
jira issue link

# Create block relationship
jira issue link PROJ-123 PROJ-456 Blocks

# Link as duplicate
jira issue link PROJ-123 PROJ-456 Duplicates

# General relation
jira issue link PROJ-123 PROJ-456 "Relates to"
```

## Unlink Issues

```bash
jira issue unlink <SOURCE-KEY> <TARGET-KEY>
```

```bash
# Interactive unlinking
jira issue unlink

# Remove link
jira issue unlink PROJ-123 PROJ-456
```

## Add Remote Link

```bash
jira issue link remote <ISSUE-KEY> <URL> [TITLE]
```

```bash
# Add link to PR
jira issue link remote PROJ-123 "https://github.com/org/repo/pull/456" "PR #456"

# Add link to documentation
jira issue link remote PROJ-123 "https://docs.example.com/feature" "Feature Docs"
```

## Worklog (Time Tracking)

```bash
jira issue worklog add [ISSUE-KEY] [TIME-SPENT]
```

### Time Format

| Format   | Meaning                   |
| -------- | ------------------------- |
| `30m`    | 30 minutes                |
| `2h`     | 2 hours                   |
| `1d`     | 1 day (typically 8 hours) |
| `1w`     | 1 week (typically 5 days) |
| `2h 30m` | 2 hours and 30 minutes    |
| `1d 4h`  | 1 day and 4 hours         |

### Options

| Flag               | Description                     |
| ------------------ | ------------------------------- |
| `--comment <text>` | Add description for the worklog |
| `--no-input`       | Disable interactive prompts     |

### Examples

```bash
# Interactive worklog
jira issue worklog add
jira issue worklog add PROJ-123

# Add worklog directly
jira issue worklog add PROJ-123 "2h 30m" --no-input

# Worklog with comment
jira issue worklog add PROJ-123 "1d" --comment "Backend implementation" --no-input

# Quick time logging
jira issue worklog add PROJ-123 "30m" --comment "Code review" --no-input
```

## Clone Issue

```bash
jira issue clone <ISSUE-KEY> [options]
```

### Options

| Flag                           | Description                         |
| ------------------------------ | ----------------------------------- |
| `-s, --summary <text>`         | Override summary                    |
| `-y, --priority <priority>`    | Override priority                   |
| `-a, --assignee <user>`        | Override assignee                   |
| `-l, --label <label>`          | Override labels                     |
| `-H, --replace <find:replace>` | Replace text in summary/description |

### Examples

```bash
# Simple clone
jira issue clone PROJ-123

# Clone with modifications
jira issue clone PROJ-123 \
  -s"[Clone] Original summary" \
  -yMedium \
  -a$(jira me)

# Clone with text replacement
jira issue clone PROJ-123 -H"production:staging"

# Clone for different environment
jira issue clone PROJ-123 \
  -s"[Staging] Deploy feature X" \
  -H"production:staging" \
  --label staging
```

## Delete Issue

```bash
jira issue delete [ISSUE-KEY]
```

### Options

| Flag        | Description              |
| ----------- | ------------------------ |
| `--cascade` | Delete with all subtasks |

### Examples

```bash
# Interactive deletion
jira issue delete

# Delete specific issue
jira issue delete PROJ-123

# Delete with subtasks
jira issue delete PROJ-123 --cascade
```

## Best Practices

1. **Use `--no-input`** for all scripted operations
2. **Show current state** before editing:

   ```bash
   jira issue view PROJ-123
   ```

3. **Confirm changes** with user before executing
4. **Use `-` prefix** correctly for removals
5. **Quote text values** containing spaces or special characters
6. **Handle errors** gracefully with user-friendly messages

## Common Patterns

### Update Priority Based on Severity

```bash
# Escalate to high priority
jira issue edit PROJ-123 -yHigh --label escalated --no-input

# De-escalate
jira issue edit PROJ-123 -yLow --label -escalated --no-input
```

### Start Working on Issue

```bash
# Assign to self, move to In Progress, log start
jira issue assign PROJ-123 $(jira me)
jira issue move PROJ-123 "In Progress" --comment "Starting work"
```

### Complete Issue with Time Log

```bash
# Log time and close
jira issue worklog add PROJ-123 "4h" --comment "Implementation" --no-input
jira issue move PROJ-123 Done -RFixed --comment "Completed"
```

### Bulk Label Management

```bash
# Add sprint label to multiple issues
for issue in PROJ-123 PROJ-124 PROJ-125; do
  jira issue edit "$issue" --label sprint-42 --no-input
done
```

### Transfer Between Components

```bash
jira issue edit PROJ-123 \
  --component -Frontend \
  --component Backend \
  --label needs-review \
  --no-input
```

### Close as Duplicate

```bash
# Link to original issue
jira issue link PROJ-123 PROJ-100 Duplicates

# Close with resolution (if available in workflow)
jira issue move PROJ-123 Done -RDuplicate --comment "Duplicate of PROJ-100"

# Or without resolution (for workflows that don't support it)
jira issue move PROJ-123 Done --comment "Duplicate of PROJ-100"
```
