# Updating Items

How to update request-log items: change status, add notes, modify fields.

---

## CLI Commands

Two commands for updating items:

| Command | Purpose |
|---------|---------|
| `log note add` | Add a note to an item |
| `log item update` | Update item fields (status, priority, tags, etc.) |

---

## Update Item Status

The most common operation - changing item status as work progresses:

```bash
# Mark as in-progress when starting work
meatycapture log item update REQ-20260105-project.md ITEM-01 --status in-progress

# Mark as done when complete
meatycapture log item update REQ-20260105-project.md ITEM-01 --status done

# Mark as wontfix (add note explaining why)
meatycapture log item update doc.md ITEM-01 --status wontfix
meatycapture log note add doc.md ITEM-01 -c "Duplicate of ITEM-03"
```

### Status Values

| Status | Description |
|--------|-------------|
| `triage` | New item, needs review and prioritization |
| `backlog` | Reviewed, accepted, not yet scheduled |
| `planned` | Scheduled for upcoming work |
| `in-progress` | Currently being worked on |
| `done` | Completed |
| `wontfix` | Closed without action (duplicate, invalid, deferred) |

### Typical Transitions

```
triage -> backlog -> planned -> in-progress -> done
                 \-> wontfix (at any stage)
```

---

## Add Notes

Add context, updates, or resolution info to items:

```bash
# Basic note
meatycapture log note add doc.md ITEM-01 --content "Investigating root cause"

# Short form
meatycapture log note add doc.md ITEM-01 -c "Fixed in PR #456"

# With note type
meatycapture log note add doc.md ITEM-01 -c "Attempted fix but tests fail" -t "Bug Fix Attempt"
meatycapture log note add doc.md ITEM-01 -c "Verified fix in staging" -t "Validation"
```

### Note Types

| Type | Use For |
|------|---------|
| `General` | Default - general updates, context |
| `Bug Fix Attempt` | Recording fix attempts (successful or not) |
| `Validation` | Verification, testing notes |
| `Other` | Anything else |

---

## Update Other Fields

### Priority

```bash
meatycapture log item update doc.md ITEM-01 --priority critical
meatycapture log item update doc.md ITEM-01 --priority high
meatycapture log item update doc.md ITEM-01 --priority medium
meatycapture log item update doc.md ITEM-01 --priority low
```

### Type

```bash
meatycapture log item update doc.md ITEM-01 --type bug
meatycapture log item update doc.md ITEM-01 --type enhancement
meatycapture log item update doc.md ITEM-01 --type task
```

### Tags

```bash
# Replace all tags
meatycapture log item update doc.md ITEM-01 --tags "security,critical"

# Add tags (preserves existing)
meatycapture log item update doc.md ITEM-01 --add-tags "reviewed,approved"

# Remove tags
meatycapture log item update doc.md ITEM-01 --remove-tags "triage,needs-review"
```

### Title, Domain, Context

```bash
meatycapture log item update doc.md ITEM-01 --title "Updated title here"
meatycapture log item update doc.md ITEM-01 --domain api
meatycapture log item update doc.md ITEM-01 --context "auth-service"
```

---

## Multiple Updates at Once

Combine options in a single command:

```bash
meatycapture log item update doc.md ITEM-01 \
  --status in-progress \
  --priority high \
  --add-tags "sprint-5"
```

---

## Path Resolution

Commands support project-aware path resolution. For files matching `REQ-YYYYMMDD-<project>.md`:

```bash
# These are equivalent if project is configured:
meatycapture log item update REQ-20260105-meatycapture.md ITEM-01 --status done
meatycapture log item update ~/.meatycapture/docs/meatycapture/REQ-20260105-meatycapture.md ITEM-01 --status done
```

---

## Common Workflows

### Bug Resolution

```bash
# 1. Start working on bug
meatycapture log item update doc.md ITEM-01 --status in-progress

# 2. Note your progress
meatycapture log note add doc.md ITEM-01 -c "Root cause: missing null check in parser"

# 3. Note the fix
meatycapture log note add doc.md ITEM-01 -c "Fixed in commit abc123, PR #456" -t "Bug Fix Attempt"

# 4. Mark as done
meatycapture log item update doc.md ITEM-01 --status done
```

### Triage Review

```bash
# Promote from triage to backlog after review
meatycapture log item update doc.md ITEM-01 --status backlog --priority medium

# Or close as wontfix
meatycapture log item update doc.md ITEM-01 --status wontfix
meatycapture log note add doc.md ITEM-01 -c "Out of scope for MVP"
```

### Sprint Planning

```bash
# Move items to planned for next sprint
meatycapture log item update doc.md ITEM-01 --status planned --add-tags "sprint-6"
meatycapture log item update doc.md ITEM-02 --status planned --add-tags "sprint-6"
```

---

## Output Formats

```bash
# Default human-readable output
meatycapture log item update doc.md ITEM-01 --status done

# JSON output for scripting
meatycapture log item update doc.md ITEM-01 --status done --json

# YAML output
meatycapture log item update doc.md ITEM-01 --status done --yaml
```

---

## Verification

After updating, verify the change:

```bash
# View updated item
meatycapture log view doc.md --json | jq '.items[] | select(.id == "ITEM-01")'

# Check item status
meatycapture log view doc.md --json | jq '.items[] | {id: .id, status: .status}'
```

---

## Backup

By default, commands create a `.bak` backup before modifying files:

```bash
# Disable backup (use with caution)
meatycapture log item update doc.md ITEM-01 --status done --no-backup
meatycapture log note add doc.md ITEM-01 -c "Note" --no-backup
```
