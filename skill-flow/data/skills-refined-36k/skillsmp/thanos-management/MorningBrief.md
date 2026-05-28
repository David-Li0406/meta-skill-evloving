# Morning Brief Protocol

## Purpose
On first session of each day, proactively brief Jeremy on his day before he has to ask.

---

## Trigger Conditions

Activate morning brief when:
- First message of the day (check: no session log for today yet)
- Time is between 5:00 AM and 12:00 PM
- User activates Thanos mode

---

## Morning Brief Format

```
═══════════════════════════════════════
    THANOS ACTIVATED - THANOS ONLINE
═══════════════════════════════════════

**[{TIME} EST] - {DAY}, {DATE}**

**COMMITMENTS DUE TODAY:**
{list from Commitments.md where deadline = today}

**TOP 3 PRIORITIES:**
1. {from CurrentFocus.md or inferred}
2. {priority 2}
3. {priority 3}

**WAITING FOR:**
{any items from WaitingFor.md due for follow-up}

**YESTERDAY'S INCOMPLETE:**
{carried over from previous Today.md}

**ENERGY CHECK:**
What's your energy level (1-10)?

**RECOMMENDED FIRST ACTION:**
{highest priority actionable item}

---
You are someone who starts days with clarity. Act accordingly.
```

---

## Data Sources

| Section | Source |
|---------|--------|
| Commitments Due | State/Commitments.md (filter by today's date) |
| Top 3 Priorities | State/CurrentFocus.md → Today's Top 3 |
| Waiting For | State/WaitingFor.md (items needing follow-up) |
| Yesterday's Incomplete | Previous day's Today.md unchecked items |
| Calendar | GSuite MCP if available |

---

## Generation Process

1. **Query Time**: Confirm it's morning, first session
2. **Read State Files**:
   - State/Today.md (or yesterday's if today's doesn't exist)
   - State/CurrentFocus.md
   - State/Commitments.md
   - State/WaitingFor.md
   - State/ThisWeek.md
3. **Query Memory**: Claude Flow memory for recent patterns
4. **Check Calendar**: GSuite MCP for today's events (if connected)
5. **Generate Brief**: Compile into format above
6. **Create Today.md**: Generate fresh Today.md for current date
7. **Ask Energy**: Prompt for energy level to calibrate recommendations

---

## Energy-Based Recommendations

After user provides energy level:

| Energy | Recommendation |
|--------|----------------|
| 1-3 | "Low energy. Do ONE easy win first to build momentum. Consider: {easiest task}" |
| 4-6 | "Moderate energy. Start with {medium priority} to warm up, then tackle {top priority}" |
| 7-10 | "High energy. Attack {hardest/most important task} now while you have capacity" |

---

## Post-Brief Actions

1. Update State/Today.md with:
   - Current date
   - Energy level (once captured)
   - Vyvanse status (ask if not mentioned)
   - Priorities for day
2. Store morning state in Claude Flow memory
3. Set context for OPERATOR mode for rest of day

---

## Example Morning Brief

```
═══════════════════════════════════════
    THANOS ACTIVATED - THANOS ONLINE
═══════════════════════════════════════

**[07:15 EST] - Monday, January 6, 2026**

**COMMITMENTS DUE TODAY:**
- Baptist status report | Baptist team | EOD
- Follow up on ScottCare interface | Client | EOD

**TOP 3 PRIORITIES:**
1. Complete Baptist status report (started yesterday)
2. ScottCare provider matching resolution
3. Invoice review for December

**WAITING FOR:**
- Memphis: Response on interface spec (sent Jan 3)

**YESTERDAY'S INCOMPLETE:**
- Daily energy logging (skipped)

**ENERGY CHECK:**
What's your energy level (1-10)?

**RECOMMENDED FIRST ACTION:**
Open Baptist report doc and finish final section.

---
You are someone who starts days with clarity. Act accordingly.
```

---

## Integration Notes

- Runs automatically on Thanos activation if morning
- No permission needed - just executes
- Creates Today.md if doesn't exist
- Updates existing Today.md if already created
- Stores brief in session log
