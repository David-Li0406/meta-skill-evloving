# Commitment Auto-Extraction Protocol

## Purpose
Automatically detect when Jeremy makes a commitment during conversation and add it to State/Commitments.md

---

## Detection Patterns

### Explicit Commitment Phrases
```
"I'll do {X} by {time/date}"
"I'll have {X} done by {time/date}"
"I committed to {X}"
"I promised {person} I'd {X}"
"Tell {person} I'll {X}"
"By {time/date} I need to {X}"
"I'm going to {X} tomorrow/today/this week"
"I'll get {X} to {person}"
"I'll send {X} by {time/date}"
"I'll follow up on {X}"
```

### Implicit Commitment Indicators
```
"I should {X}" + confirmation
"I need to {X}" + time reference
"Remind me to {X}"
"{Person} is expecting {X}"
"I owe {person} {X}"
```

### Work-Specific Patterns
```
"I'll have the {deliverable} ready"
"{Client} needs {X} by {date}"
"The interface will be done by..."
"I'll send the status report"
```

---

## Extraction Process

1. **Detect**: Pattern match against conversation
2. **Parse**: Extract components:
   - What: The specific deliverable/action
   - To Whom: Person, client, or self
   - By When: Deadline (explicit or inferred)
   - Context: Why it matters, related project
3. **Confirm**: Brief confirmation (not a question, just acknowledgment)
   - "Logged: {commitment summary} by {deadline}"
4. **Store**: Add to State/Commitments.md in appropriate section
5. **Memory**: Store in Claude Flow for cross-session tracking

---

## Commitment Entry Format

```markdown
- [ ] {What} | {To Whom} | {By When} | {Status}
  - Context: {additional details}
  - Source: Session {date}
```

---

## Auto-Categorization

Route to correct section in Commitments.md:

| To Whom | Section |
|---------|---------|
| Memphis, Raleigh, Orlando, Nova, Baptist, ScottCare | Work Commitments → {Client} |
| Ashley | Personal Commitments → Ashley |
| Sullivan, Family | Personal Commitments → Family |
| Self | Commitments to Self |
| Other person | Personal Commitments → Other |

---

## Deadline Inference

When no explicit deadline given:

| Phrase | Inferred Deadline |
|--------|-------------------|
| "today" | Today EOD |
| "tomorrow" | Tomorrow EOD |
| "this week" | Friday EOD |
| "next week" | Next Friday |
| "soon" | +3 days (flag for clarification) |
| No time reference | Ask: "By when?" |

---

## Example Interactions

**User:** "I'll have the Baptist status report done by end of day tomorrow"

**System Response:**
"Logged: Baptist status report | Baptist team | Tomorrow EOD"

**Auto-added to Commitments.md:**
```markdown
### Baptist Rehab
- [ ] Status report | Baptist team | 2026-01-06 EOD | Not Started
  - Context: Optimization project update
  - Source: Session 2026-01-05-2211
```

---

**User:** "Tell Ashley I'll handle the formula restocking"

**System Response:**
"Logged: Formula restocking | Ashley | Today"

**Auto-added to Commitments.md:**
```markdown
### Ashley
- [ ] Formula restocking | Ashley | 2026-01-05 | Not Started
  - Context: Sullivan supplies
  - Source: Session 2026-01-05-2211
```

---

## Integration Notes

- Run detection continuously during conversation
- Silent logging (no verbose confirmations)
- Brief acknowledgment only: "Logged: {summary}"
- On session end, include all extracted commitments in session log
