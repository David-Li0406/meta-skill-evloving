# Issue Template

Issues are stored in `.agent/issues/` by priority level.

## Issue ID Format

`{TYPE}-{NUMBER}@{HASH}`

- **TYPE**: `BUG` | `FEAT` | `CHORE` | `ENH` | `SEC` | `PERF` | `DOCS` | `TEST` | `REFAC` | `PLAN`
- **NUMBER**: 4-digit incrementing (from `.agent/issues/.counter`)
- **HASH**: 6-character random hex

Example: `FEAT-0042@c2d4e6`

## Issue Structure

```yaml
## {TYPE}-{NUMBER}@{HASH} — {title}

id: {TYPE}-{NUMBER}@{HASH}
title: "{short title}"
type: bug | feat | chore | enh | sec | perf | docs | test | refac | plan
status: todo | in_progress | blocked | done | cancelled | dropped
priority: critical | high | medium | low
epic: ""  # optional grouping, e.g., "Authentication", "Q1 Launch", "Tech Debt"
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
- YYYY-MM-DD: {update}
```

## File Locations

| Priority | File |
|----------|------|
| critical | `.agent/issues/critical.md` |
| high | `.agent/issues/high.md` |
| medium | `.agent/issues/medium.md` |
| low | `.agent/issues/low.md` |
| archived | `.agent/issues/history.md` |
| specs | `.agent/issues/references/{ISSUE-ID}.md` |
