# Change Log Format

Specification for tracking changes made during document polishing.

## Purpose

Maintain an audit trail of all modifications for:
- Transparency (user knows what changed)
- Debugging (identify if a fix caused issues)
- Undo capability (revert specific changes if needed)

## Change Entry Format

Each change is recorded as a JSON object:

```json
{
  "id": "unique-change-id",
  "phase": 1|2|3,
  "iteration": 1,
  "timestamp": "ISO-8601",
  "issue_type": "type from enum",
  "location": "line number or section",
  "action": "what was changed",
  "before": "original text (truncated if >100 chars)",
  "after": "new text (truncated if >100 chars)",
  "source": "claude|codex|user"
}
```

## Field Descriptions

| Field | Description |
|-------|-------------|
| `id` | Unique identifier for this change (e.g., `p1-i2-c3` = Phase 1, Iteration 2, Change 3) |
| `phase` | Which phase made this change (1, 2, or 3) |
| `iteration` | Iteration number within the phase |
| `timestamp` | When the change was made |
| `issue_type` | Type from issue-criteria.md enumeration |
| `location` | Where in the document (line number, section heading) |
| `action` | Brief description of what was done |
| `before` | Original text before change |
| `after` | New text after change |
| `source` | Who/what made the change |

## In-Memory Structure

During execution, maintain change log as array:

```
change_log = []

# After each fix, append:
change_log.append({
  "id": f"p{phase}-i{iteration}-c{len(change_log)+1}",
  "phase": phase,
  "iteration": iteration,
  "timestamp": now(),
  "issue_type": issue.type,
  "location": issue.location,
  "action": fix_description,
  "before": truncate(original_text, 100),
  "after": truncate(new_text, 100),
  "source": "claude"|"codex"|"user"
})
```

## Final Report Integration

Include change summary in final report:

```
╠══════════════════════════════════════════════════════════════╣
║ CHANGE LOG                                                   ║
╟──────────────────────────────────────────────────────────────╢
║ Total changes: 5                                             ║
║                                                              ║
║ [p1-i1-c1] inconsistent_terminology @ line 12                ║
║   "user" → "customer" (standardized)                         ║
║                                                              ║
║ [p1-i1-c2] redundant_content @ section "Overview"            ║
║   Removed duplicate paragraph                                ║
║                                                              ║
║ [p2-i1-c3] formatting_inconsistency @ lines 45-50            ║
║   Mixed bullets → standardized to "-"                        ║
║                                                              ║
║ [p3-i1-c4] vague_instruction @ line 78                       ║
║   "handle appropriately" → "log error and retry 3x"          ║
║                                                              ║
║ [p3-i1-c5] unresolved_todo @ line 92                         ║
║   "TODO: caching" → "No caching for MVP"                     ║
╚══════════════════════════════════════════════════════════════╝
```

## Usage Notes

- Change log is kept in memory during execution
- Included in final report for user review
- Can be used for "undo last change" if implemented
- Truncate long text to keep report readable
