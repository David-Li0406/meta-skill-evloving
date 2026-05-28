# Session Logging Protocol

## Purpose
Capture every conversation session to History/Sessions/ for pattern analysis and context preservation.

---

## Session End Trigger

Activate when:
- User says "goodnight", "going to bed", "closing out", "done for now"
- User invokes `/close` or `/end`
- Explicit session end detected

---

## Session Log Format

**File:** `History/Sessions/YYYY-MM-DD-HHMM.md`

```markdown
# Session: {date} {time}

## Duration
- Started: {start_time}
- Ended: {end_time}
- Length: {duration}

## Summary
{2-3 sentence summary of what was accomplished}

## Topics Covered
- {topic 1}
- {topic 2}
- {topic 3}

## Commitments Made
- [ ] {commitment 1} | Due: {date} | To: {person/self}
- [ ] {commitment 2} | Due: {date} | To: {person/self}

## Decisions Made
- {decision 1}: {brief reasoning}
- {decision 2}: {brief reasoning}

## State Changes
- Updated: {list of State/ files modified}
- Created: {list of new files}

## Follow-ups Needed
- {item requiring future attention}

## Mood/Energy (if captured)
- Energy level: {1-10}
- Mood: {brief descriptor}

---
*Auto-logged by Thanos*
```

---

## Implementation

**On Session End:**

1. Query Claude Flow memory for session context
2. Extract commitments using patterns (see CommitmentExtraction.md)
3. Identify decisions made
4. List State/ files that were modified
5. Generate 2-3 sentence summary
6. Write to History/Sessions/{timestamp}.md
7. Store summary in Claude Flow memory for cross-session access
8. Execute git sync: `bash /Users/jeremy/.claude/Tools/sync-thanos.sh`

**Memory Storage:**
```
namespace: sessions
key: {YYYY-MM-DD-HHMM}
value: {summary + key metadata}
```

---

## Integration with Thanos

Add to session end behavior:
- Silent execution (no confirmation needed)
- Auto-generate without prompting user
- Store in both file system AND Claude Flow memory
