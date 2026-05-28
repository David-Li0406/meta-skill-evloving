# Issue Management Reference

Extended reference documentation for `agent-ops-tasks` skill.

---

## File-Based Operations (Default)

All issue operations can be performed via direct file editing:

| Operation | How to Do It |
|-----------|--------------|
| List issues | Read `.agent/issues/{priority}.md` files directly |
| Show issue | Search for issue ID in priority files |
| Create issue | Increment `.counter`, append to `.agent/issues/{priority}.md` |
| Update issue | Edit fields directly in the file |
| Close issue | Set `status: done`, add log entry, move to `history.md` |
| Summary view | Count issues across priority files |

---

## CLI Commands (Optional — when aoc is available)

When `aoc` CLI is detected in `.agent/tools.json`, these commands provide convenience shortcuts:

| Command | Description | Example |
|---------|-------------|---------|
| `aoc issues list` | List all issues | `aoc issues list --priority high --status todo` |
| `aoc issues show <ID>` | Show issue details | `aoc issues show FEAT-0001@abc123` |
| `aoc issues create` | Create new issue | `aoc issues create --type BUG --priority high` |
| `aoc issues update <ID>` | Update issue | `aoc issues update BUG-0042 --status in-progress` |
| `aoc issues close <ID>` | Close issue | `aoc issues close BUG-0042 --log "Fixed"` |
| `aoc issues summary` | Summary view | `aoc issues summary` |
| `aoc issues kanban` | Kanban view | `aoc issues kanban` |

### Filter Examples

```bash
aoc issues list --priority high --type BUG
aoc issues list --epic "auth" --status open
aoc issues list --json > issues.json
```

---

## Issue Template (Full)

```yaml
## {TYPE}-{NUMBER}@{HASH} — {title}

id: {TYPE}-{NUMBER}@{HASH}
title: "{short title}"
type: bug | feat | chore | enh | sec | perf | docs | test | refac | plan
status: todo | in_progress | blocked | done | cancelled | dropped
priority: critical | high | medium | low | backlog
epic: ""
created: YYYY-MM-DD
updated: YYYY-MM-DD
owner: agent | human | {name}
confidence: low | normal | high

### Scope
files_to_change:
  - path/to/file.ts
files_must_not_change:
  - path/to/protected.ts

### Requirements
- Requirement 1
- Requirement 2

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

### Dependencies
depends_on:
  - {ISSUE-ID}
blocks:
  - {ISSUE-ID}

### References
spec_file: .agent/issues/references/{ISSUE-ID}.md

### Notes
{Additional context}

### Log
- YYYY-MM-DD: Created
```

---

## BUG Issue Template

```yaml
## BUG-{NUMBER}@{HASH} — {title}

id: BUG-{NUMBER}@{HASH}
title: "{bug description}"
type: BUG
status: todo | in_progress | done
priority: critical | high | medium | low
epic: ""
created: YYYY-MM-DD
updated: YYYY-MM-DD
owner: agent
confidence: low | normal | high

### Problem
{What was broken? Symptoms? Root cause?}

### Scope
files_to_change:
  - path/to/affected.ts

### Acceptance Criteria
- [ ] Bug no longer reproduces
- [ ] Tests added to prevent regression

### Solution
{Populated when done - what fixed it and why}

### Log
- YYYY-MM-DD: Created
- YYYY-MM-DD: Fixed - {summary}
```

---

## Type Prefixes

| Prefix | Description |
|--------|-------------|
| `BUG` | Bug fix |
| `FEAT` | New feature |
| `CHORE` | Maintenance |
| `ENH` | Enhancement |
| `SEC` | Security |
| `PERF` | Performance |
| `DOCS` | Documentation |
| `TEST` | Test coverage |
| `REFAC` | Refactor |
| `PLAN` | Epic/plan |

---

## JSON Export

### Export Command

```bash
aoc issues json --priority critical,high --output issues.json
```

### JSON Structure

```json
{
  "exported": "2026-01-15T10:30:00Z",
  "filters": {"priority": ["critical", "high"]},
  "count": 7,
  "issues": [
    {
      "id": "BUG-0023@efa54f",
      "type": "BUG",
      "priority": "high",
      "title": "Fix login timeout",
      "status": "open",
      "created": "2026-01-10"
    }
  ]
}
```

---

## Discovery Output Format

When skills call discovery:

```yaml
findings:
  - type: bug
    priority: high
    title: "Fix failing test: UserService.login"
    context: "Test started failing after baseline"
    files: [src/services/UserService.ts]
```

---

## Quick Triage Shorthand

```bash
aoc issues triage              # Interactive
aoc issues triage IDEA-0001 high  # Direct
```

---

## Bulk Operations

```bash
# Batch mode
aoc issues batch
> bug high "Fix session expiry"
> feat medium "Add remember me"
> done
```

---

## Schema Validation Errors

| Error | Fix |
|-------|-----|
| Missing `id` | Generate new ID |
| Invalid ID format | Correct to `TYPE-NNNN@HHHHHH` |
| Invalid type | Use standard prefix |
| Missing status | Add `status: todo` |
