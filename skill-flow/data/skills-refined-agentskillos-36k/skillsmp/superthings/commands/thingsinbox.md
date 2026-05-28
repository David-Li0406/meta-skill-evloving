---
name: thingsinbox
description: Triage and organize Things inbox with learned patterns that improve from corrections over time
model: haiku
---

# Things Inbox Triage

Triage and organize the Things inbox by cleaning up task titles and assigning them to appropriate projects. **Uses learned patterns from your corrections to get better over time.**

## Learning System (Agent-Native)

The learning system is now fully agent-native using MCP tools:

| Tool | Purpose |
|------|---------|
| `things_suggest_for_task` | Get suggestion + confidence for a task title |
| `things_list_patterns` | View all learned patterns |
| `things_log_correction` | Log a single correction |
| `things_learn_batch` | Log multiple decisions at once |

**Pattern priority order:**
1. `exact_overrides` (exact title match)
2. `title_transforms` (regex pattern match)
3. `project_hints` (keyword-based)
4. Hardcoded defaults (below)

## Confidence Thresholds

| Confidence | Behavior |
|------------|----------|
| >= 10 | Apply silently (trusted pattern) |
| >= 3 | Auto-apply with `[learned: Nx]` indicator |
| < 3 | **Use AskUserQuestion** with context |

## Workflow

### 1. Fetch Inbox
Call `mcp__SuperThings__things_get_inbox` directly (server handles caching with 1-minute TTL).

### 2. Get Suggestions for Each Task
For each inbox item, call `things_suggest_for_task` to get:
- `suggested_title`: The recommended title
- `suggested_project`: The recommended project
- `confidence`: 0-10 score
- `pattern_source`: Where the suggestion came from
- `examples`: Previous tasks that matched this pattern

### 3. Handle Low-Confidence Items (< 3)

**Use AskUserQuestion** when confidence is below 3:

```
AskUserQuestion:
  questions:
    - question: "Title suggestion for '[ORIGINAL_TITLE]'?"
      header: "[N]x"  # confidence score
      multiSelect: false
      options:
        - label: "[SUGGESTED_TITLE]"
          description: "Pattern: [PATTERN_RULE] | [N]x confidence | Examples: [EX1], [EX2]"
        - label: "[ORIGINAL_TITLE]"
          description: "Keep original unchanged"
        - label: "Custom..."
          description: "Type a different title"
```

**Example:**
```
question: "Title suggestion for 'Fix fireplace'?"
header: "2x"
options:
  - label: "Delegate to Brianna: Fix fireplace"
    description: "Pattern: ^Fix → Delegate | 2x confidence | Examples: Fix garage, Fix dishwasher"
  - label: "Fix fireplace"
    description: "Keep original unchanged"
```

### 4. Process Tasks by Type

**URL tasks** - Use WebFetch to resolve URLs:
- YouTube: "Watch: [Video Title] - [Creator]"
- GitHub: "Review: [Repo Name] - [Description]"
- Google Maps: "Visit: [Place Name]"
- Article: "Read: [Article Title]"
- **Move original URL to notes field**

**Clear tasks** - Keep title as-is, just categorize

**Unclear/cryptic tasks** - Leave title unchanged (don't guess)

### 5. Assign Projects

**Default: Computer** - Almost everything goes here if doable on computer OR delegated.

| Pattern | Project |
|---------|---------|
| Research, Email, Intro, Follow up, Draft, Buy, Book, Schedule, Review, Check, Order, Send, Create, Find, Watch, Read | Computer (`LDhUsibk3dp2ZPioQySSiu`) |
| Fix, maintenance, home repairs | Computer - Reformat as "Delegate to Brianna: [task]" |
| Call [person], Phone call required | Call (`Er67bc9YAur6ZeKTCBLC4c`) |
| Physical in-person errands only | Out and About (`5LwYiPJAkWGSCMHML8xaXb`) |
| Kid-specific activities | Kids/Activities (`7n14Jusf7nCrLADfAANabW`) |
| **Build/Make [software]** | Deep Work (`WamuBi2sFwbUwpXz9NZetP`) |
| Long-form writing (1+ hour focused) | Deep Work (`WamuBi2sFwbUwpXz9NZetP`) |

**Build/Make → Deep Work**: Apps, plugins, tools, bots, systems, integrations, APIs, scrapers, workflows, pipelines, anything requiring hours of coding.

**Exceptions (stay in Computer)**: "Build a list of...", "Build rapport with...", "Make a reservation...", "Make an intro..."

**Rules**:
- When in doubt → Computer
- NEVER assign to Someday unless user explicitly asks
- Fix/maintenance → "Delegate to Brianna: [task]" → Computer
- Research → Always Computer (never Deep Work)

### 6. Present Results

Use grouped card format:
```
Inbox (44) | C=Computer D=Deep O=Out P=Call

┌─ 1 ─────────────────────────────────────────────────── C ✎
│  https://youtu.be/pE3KKUKXcTM...
│  ↓
│  Watch: Semiconductor Industry Works
├─ 2 ─────────────────────────────────────────────────── C ✎
│  Fix fireplace
│  ↓
│  Delegate to Brianna: Fix fireplace        [learned: 12x]
├─ 3 ─────────────────────────────────────────────────── C
│  Research competitor pricing
├─ 4 ─────────────────────────────────────────────────── P
│  Call dentist
```

**Format rules:**
- Card header: `┌─ # ───...─── X ✎` where X is project code, ✎ if title changes
- `[learned: Nx]` when suggestion comes from learned patterns
- Project codes: C=Computer, D=Deep, O=Out&About, P=Call, K=Kids

### 7. Show Preview Summary

```
─────────────────────────────────────────────────────────────
Preview: 12 items
├─ 3 title rewrites (✎)
├─ 8 project moves
├─ 1 delegation
└─ 2 learned patterns applied

Reply: numbers (1,3,5-8), "all", "skip N", or "S3" to snooze
```

### 8. Wait for User Approval

User replies with:
- Numbers: `1,3,5-8` - approve specific items
- `all` - approve everything
- `skip N` - approve all except item N
- `S3` or `snooze 3` - snooze item 3 for 1 week
- `S3 2w` - snooze item 3 for 2 weeks
- `S3 1m` - snooze item 3 for 1 month

**Snooze behavior:**
- Sets `when` to future date, removes from inbox
- Item reappears in Today on the scheduled date

### 9. Save Undo State

**BEFORE executing updates**, save state:
```bash
echo '[
  {"id":"ID1","original_title":"ORIG1","original_list":"inbox"},
  {"id":"ID2","original_title":"ORIG2","original_list":"inbox"}
]' > ~/claudesync/servers/super-things/data/last_triage.json
```

### 10. Execute Updates

Use `mcp__SuperThings__things_update_todo` for approved items.

For snoozed items:
```
mcp__SuperThings__things_update_todo with:
  id: <item_id>
  when: <date N days from now in YYYY-MM-DD format>
```

### 11. Log and Learn (MANDATORY)

**Use `things_learn_batch`** to log all decisions at once:

```
things_learn_batch with decisions: [
  {
    "original_title": "Fix fireplace",
    "suggested_title": "Delegate to Brianna: Fix fireplace",
    "final_title": "Delegate to Brianna: Fix fireplace",
    "suggested_project": "Computer",
    "final_project": "Computer",
    "title_accepted": true,
    "project_accepted": true
  },
  ...
]
```

This automatically:
- Appends to history.jsonl
- Increments confidence for accepted patterns
- Learns new patterns from corrections
- Updates project hints

**Skip learning only if:** User explicitly cancels or no items were processed.

## URL Resolution

For URL tasks, use **WebFetch** to resolve:
1. Fetch URL content
2. Extract title and description
3. Create actionable task title
4. Move original URL to notes field

Launch parallel agents (haiku model) for multiple URLs.

## Project IDs Reference

- Computer: `LDhUsibk3dp2ZPioQySSiu`
- Deep Work: `WamuBi2sFwbUwpXz9NZetP`
- Call: `Er67bc9YAur6ZeKTCBLC4c`
- Home: `NsSR9HR3pd2bVi2z4QHFfM`
- Out and About: `5LwYiPJAkWGSCMHML8xaXb`
- Kids/Activities: `7n14Jusf7nCrLADfAANabW`
- Someday: `EZ5uJWRtcrvJ4U852NkNQ8`

## Undo Last Triage

If user says "undo" or "revert":

1. Read `~/claudesync/servers/super-things/data/last_triage.json`
2. For each item, restore with `things_update_todo`:
   - title: original_title
   - list: "inbox"
3. Confirm: "Reverted N items to their original state"
4. Clear the undo file: `echo '[]' > ~/claudesync/servers/super-things/data/last_triage.json`

**Note:** Only the LAST triage batch can be undone.

## Model Escalation

Runs on Haiku, but **auto-escalates to Sonnet** for:
- Unclear/cryptic tasks requiring judgment
- Complex categorization decisions
- "Get stuff done" execution mode

Use Task tool with `model: sonnet` for complex items.

## Execution Checklist

1. Fetch inbox with `things_get_inbox`
2. For each item, call `things_suggest_for_task`
3. If confidence < 3, use AskUserQuestion with context
4. If confidence >= 3, auto-apply with `[learned: Nx]`
5. Present card format preview
6. Wait for user approval
7. Save undo state
8. Execute updates
9. Call `things_learn_batch` with all decisions
10. Keep responses concise to save context
