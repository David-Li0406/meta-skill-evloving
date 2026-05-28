# Reminders Reference

## Command: reminders-list

Query reminders from Apple Reminders app.

```bash
reminders-list                        # Incomplete (default)
reminders-list -a                     # All reminders
reminders-list -c                     # Only completed
reminders-list -d                     # Due today
reminders-list -o                     # Overdue
reminders-list -l "Work"              # Filter by list name
reminders-list -l "Work" -d           # Work reminders due today
reminders-list --limit 20             # Limit results
reminders-list -j                     # JSON output
```

## Examples

**"Show my overdue reminders"**
```bash
reminders-list -o
```

**"What's due today?"**
```bash
reminders-list -d
```

**"Show my Work list"**
```bash
reminders-list -l "Work"
```

## Limitations

- Large queries can timeout (10s limit)
- Use `-l` to filter by specific list if timeout occurs
- Exit code 3 = timeout
