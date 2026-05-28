# Personal Kanban

## Overview

Personal Kanban visualizes your work as cards moving across columns. Originally from manufacturing (Toyota), it's been adapted for knowledge work. You see all work at a glance and limit work-in-progress to maintain flow.

---

## The Board

### Basic Columns

```
┌─────────────┬─────────────┬─────────────┐
│   TO DO     │   DOING     │    DONE     │
├─────────────┼─────────────┼─────────────┤
│ Task A      │ Task X      │ Task Y ✓    │
│ Task B      │             │ Task Z ✓    │
│ Task C      │             │             │
│ Task D      │             │             │
└─────────────┴─────────────┴─────────────┘
```

### Enhanced Columns

```
┌─────────┬─────────┬─────────┬─────────┬─────────┐
│ BACKLOG │ TODAY   │ DOING   │ REVIEW  │  DONE   │
├─────────┼─────────┼─────────┼─────────┼─────────┤
│ Future  │ Pick    │ Focus   │ Check   │ ✓ Done  │
│ tasks   │ from    │ on ONE  │ before  │         │
│         │ here    │         │ closing │         │
└─────────┴─────────┴─────────┴─────────┴─────────┘
```

---

## Core Principles

### 1. Visualize Work
All tasks are visible as cards on the board.
- Nothing hides in your head
- Current state is obvious
- Bottlenecks are visible

### 2. Limit Work in Progress (WIP)
Restrict how many tasks can be in "DOING."
- Typical limit: 1-3 items
- Forces focus
- Prevents overwhelm
- Must finish before starting new

### 3. Flow
Work moves left to right across the board.
- No backwards movement (ideally)
- Stuck tasks are visible
- Done means done

---

## When to Use

**Good for:**
- Visual thinkers
- Multiple concurrent projects
- When you feel scattered
- Team visibility
- Long-running task tracking

**Not ideal for:**
- Very simple task lists
- When tasks are highly time-specific
- Rapid-fire short tasks

---

## How to Apply

### Step 1: Set Up Your Board
Create columns (physical or digital):
- TO DO (or BACKLOG)
- DOING (WIP limited)
- DONE

### Step 2: Add All Tasks
Write each task on a card/sticky note.
Place in TO DO column.

### Step 3: Set WIP Limit
Decide DOING limit:
- Focused: 1 item
- Normal: 2-3 items
- Max: 3-5 items (not recommended)

### Step 4: Pull Work
Move tasks from TO DO to DOING:
- Only if under WIP limit
- Choose based on priority
- Commit to what you pull

### Step 5: Finish Before Starting
Complete current DOING items before pulling new ones.
No partial work scattered across many tasks.

---

## Card Format

### Simple Card
```
┌────────────────────────┐
│ Task name              │
│                        │
│ Est: 30min   Domain: ID8│
└────────────────────────┘
```

### Detailed Card
```
┌────────────────────────┐
│ Task name              │
├────────────────────────┤
│ Domain: ID8            │
│ Project: Auth feature  │
│ Est: 2 hours           │
│ Priority: P1           │
│ Started: 2024-01-15    │
└────────────────────────┘
```

---

## Column Variations

### By Stage
```
IDEA → PLAN → DO → REVIEW → DONE
```

### By Day
```
BACKLOG → TODAY → DOING → DONE
```

### With Waiting
```
TO DO → DOING → WAITING → DONE
```
(WAITING = blocked on someone else)

### By Domain
```
ID8 Board: TO DO → DOING → DONE
TV Board: TO DO → DOING → DONE
Life Board: TO DO → DOING → DONE
```

---

## WIP Limit Deep Dive

### Why Limits Matter
Without limits:
- Start many, finish few
- Context switching kills productivity
- Nothing gets truly done
- Overwhelm builds

With limits:
- Forced to finish
- Deep focus on current work
- Clear completion
- Sustainable pace

### Setting Your Limit

| Context | Suggested WIP |
|---------|---------------|
| Deep focus day | 1 |
| Normal day | 2-3 |
| Mixed task day | 3-4 |
| Admin day | 4-5 |

Start low. Increase only if genuinely needed.

### Honoring the Limit
When DOING is full:
- Finish something first
- Don't cheat with "almost done" claims
- Blocked? Move to WAITING (doesn't count against WIP)

---

## Daily Kanban Flow

### Morning
1. Review board
2. Move yesterday's DONE to archive
3. Pull today's tasks to TO DO (daily limit)
4. Start first task → DOING

### During Day
1. Work on DOING items
2. When complete, move to DONE
3. Pull next from TO DO
4. Honor WIP limit

### Evening
1. Review what's in DOING
2. If not done, keep or return to TO DO
3. Update priorities for tomorrow

---

## Blocked Tasks

### Handling Blocks
When a task is stuck:
- Move to WAITING column
- Note what it's waiting for
- Doesn't count against WIP
- Check daily if unblocked

### WAITING Column
```
┌───────────────────────────┐
│ Task: Review with client  │
│ WAITING: Client response  │
│ Since: 2024-01-15         │
│ Follow up: 2024-01-18     │
└───────────────────────────┘
```

---

## Physical vs Digital Boards

### Physical (Sticky Notes)
**Pros:**
- Visible always
- Tactile satisfaction
- No app to open

**Cons:**
- Not portable
- Limited space
- No history

### Digital (Trello, Notion, etc.)
**Pros:**
- Portable
- Unlimited space
- History and search

**Cons:**
- Out of sight, out of mind
- Can over-complicate

### Hybrid
- Physical for daily tasks
- Digital for project/week level

---

## Combining with Other Methods

### Kanban + Eisenhower
Cards tagged by quadrant:
- Q1: Move to DOING first
- Q2: Schedule to TO DO
- Q3: Minimize
- Q4: Don't add to board

### Kanban + Pomodoro
DOING task = active pomodoro task.
Move to DONE after pomodoros complete.

### Kanban + Weekly Themes
Separate boards by theme, or tag cards by theme.

---

## Pitfalls

### 1. Too Many Columns
Board becomes bureaucracy.
**Fix:** Start with 3 columns. Add only if needed.

### 2. Ignoring WIP Limit
"Just one more in DOING..."
**Fix:** Strict limit. No exceptions.

### 3. DOING Becomes Storage
Tasks sit in DOING for days.
**Fix:** Daily review. Move back to TO DO or finish.

### 4. No Done Celebration
DONE column ignored.
**Fix:** Review DONE daily. Feel the progress.

### 5. Stale Backlog
TO DO grows infinitely.
**Fix:** Weekly purge. Delete or defer old items.

---

## Process Template

```markdown
## Personal Kanban: {date}

### Board State

**BACKLOG** (future)
- {task}
- {task}

**TODAY** (ready to pull)
- {task}
- {task}
- {task}

**DOING** (WIP: {n}/{limit})
- {task} ← IN PROGRESS
- {task}

**WAITING** (blocked)
- {task} - Waiting: {what}

**DONE** (today)
- {task} ✓
- {task} ✓

### WIP Limit: {n}
### Tasks Done Today: {count}
```

---

## Output Format

```markdown
## Kanban Board: {date}

### Current Focus
**DOING** (WIP: {n}/{limit})
┌─────────────────────────────┐
│ → {current task}            │
│   Est: {time}  Start: {time}│
└─────────────────────────────┘

### Ready to Pull
**TODAY** ({count} items)
1. {next priority}
2. {task}
3. {task}

### Blocked
**WAITING** ({count} items)
- {task} → Waiting: {what}

### Completed Today
**DONE** ({count} items)
- {task} ✓
- {task} ✓

---

**WIP Status:** {n}/{limit} - {OK/FULL}
**Next action:** {complete current OR pull next}
```
