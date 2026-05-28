---
name: superthings
description: Main command hub for SuperThings - intelligent task management with learning. Shows interactive menu for inbox triage, GTD workflows, pattern management, and stats.
---

# SuperThings Command Hub

Display the SuperThings welcome screen and interactive menu with personality and style.

## Welcome Banner

Print this ASCII art banner with rounded corners:

```
╭───────────────────────────────────────────────────────────────╮
│                                                               │
│    ✓ SuperThings                                              │
│      ─────────────                                            │
│      Intelligent task management that learns from you         │
│                                                               │
╰───────────────────────────────────────────────────────────────╯
```

## Time-Aware Greeting

**Determine the time of day and show an appropriate greeting:**

| Time | Greeting |
|------|----------|
| 5am - 11:59am | Good morning! ☀️  Ready to make today count? |
| 12pm - 4:59pm | Good afternoon! ☕  Let's knock out some tasks. |
| 5pm - 8:59pm | Good evening! 🌙  Quick triage before you unwind? |
| 9pm - 4:59am | Late night? 🦉  Dedicated! Let's make it quick. |

**Day-specific variations:**
- Monday morning: "Fresh week ahead. Let's start strong. ☀️"
- Friday afternoon/evening: "Almost weekend! Clear that inbox first? 🎉"

**After absence (if last session was 3+ days ago):** "Welcome back! Let's catch up. 👋"

## Dashboard

**Fetch counts in parallel:**
1. Call `things_get_inbox` → count items
2. Call `things_get_today` → count items
3. Read patterns from `data/patterns.json` → count patterns

**Display the dashboard:**

```
╭───────────────────────────────────────────────────────────────╮
│                                                               │
│  [GREETING GOES HERE]                                         │
│                                                               │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│    📥 Inbox          📅 Today          🧠 Patterns            │
│   ╭────────╮       ╭────────╮        ╭────────╮              │
│   │   12   │       │   8    │        │   23   │              │
│   ╰────────╯       ╰────────╯        ╰────────╯              │
│                                                               │
╰───────────────────────────────────────────────────────────────╯
```

**Replace the numbers with actual counts.**

## Main Menu

Use AskUserQuestion to show the main menu with icons:

```
question: "What would you like to do?"
header: "Menu"
multiSelect: false
options:
  - label: "📥 Triage Inbox"
    description: "Sort [N] items into projects · AI suggestions · ~3 min"
  - label: "⚡ Get Things Done"
    description: "Work through Computer & Deep Work tasks"
  - label: "🧠 Learning System"
    description: "View patterns · Stats · Manage what I've learned"
  - label: "🎯 Quick Actions"
    description: "Add · Search · Complete · Delegate"
```

**Replace [N] with actual inbox count.**

---

## Menu Actions

### Option 1: 📥 Triage Inbox

**If inbox is empty, show this fun empty state:**

```
╭───────────────────────────────────────────────────╮
│                                                   │
│  📭 Inbox Zero!                                   │
│                                                   │
│  Nothing to triage. You're all caught up.         │
│  Go outside. Touch grass. 🌿                      │
│                                                   │
╰───────────────────────────────────────────────────╯
```

**Otherwise**, run the `/thingsinbox` workflow:
- Fetch inbox items
- Apply learned patterns
- Use AskUserQuestion for low-confidence items
- Batch update decisions

**After triage completion, show celebration:**

```
╭───────────────────────────────────────────────────╮
│                                                   │
│  ✓ Inbox cleared!                                 │
│                                                   │
│  [N] items sorted · [M] patterns applied          │
│  Nice work! 🎉                                    │
│                                                   │
╰───────────────────────────────────────────────────╯
```

---

### Option 2: ⚡ Get Things Done

**If no tasks today, show:**

```
╭───────────────────────────────────────────────────╮
│                                                   │
│  📅 Nothing scheduled today                       │
│                                                   │
│  Clear calendar! Add something or just            │
│  enjoy the freedom.                               │
│                                                   │
╰───────────────────────────────────────────────────╯
```

**Otherwise**, run the `/gtd` workflow:
- Fetch Computer and Deep Work projects
- Research tasks with Tavily/Firecrawl
- Execute with C/D/DD commands

**After completing a task, show:**

```
╭───────────────────────────────────────────────────╮
│                                                   │
│  ✓ Done: "[Task Title]"                           │
│                                                   │
│  One down, [N] to go today. Keep rolling!         │
│                                                   │
╰───────────────────────────────────────────────────╯
```

---

### Option 3: 🧠 Learning System

Show the learning submenu:

```
question: "Learning System"
header: "Learn"
options:
  - label: "📊 View Patterns"
    description: "See learned title transforms and project hints"
  - label: "📈 View Stats"
    description: "Sessions, accuracy, patterns learned"
  - label: "🔧 Manage Patterns"
    description: "Remove or adjust pattern confidence"
  - label: "📜 View History"
    description: "Recent corrections and decisions"
```

#### 📊 View Patterns

Read patterns from `data/patterns.json` and display:

**If no patterns learned yet:**

```
╭───────────────────────────────────────────────────╮
│                                                   │
│  🧠 No patterns yet                               │
│                                                   │
│  I haven't learned your preferences.              │
│  Run /thingsinbox and I'll pick things up!        │
│                                                   │
╰───────────────────────────────────────────────────╯
```

**Otherwise:**

```
╭─────────────────────────────────────────────────────────────────╮
│  🧠 What I've Learned                                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TITLE PATTERNS                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  "Fix X" → "Delegate to Brianna: X"           ████████████ 12x  │
│  "Call X" → "Call: X"                         ████████░░░░  8x  │
│  "Research X" → keep as-is                    █████░░░░░░░  5x  │
│                                                                 │
│  PROJECT INTUITION                                              │
│  ─────────────────────────────────────────────────────────────  │
│  "build"    → Deep Work (15) · Computer (2)                     │
│  "research" → Computer (23) · Deep Work (1)                     │
│  "call"     → Call (18)                                         │
│                                                                 │
│  STATS                                                          │
│  ─────────────────────────────────────────────────────────────  │
│  Sessions: 47 · Items processed: 892 · Accuracy: 85%            │
│                                                                 │
╰─────────────────────────────────────────────────────────────────╯
```

**Progress bar scale:** Each █ represents ~2 uses. Max 12 blocks.

#### 📈 View Stats

Read stats from `data/patterns.json` and show:

```
╭─────────────────────────────────────────────────────────────────╮
│  📈 Learning Stats                                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Sessions Completed:  47                                        │
│  Items Processed:     892                                       │
│  Patterns Learned:    23                                        │
│                                                                 │
│  Accuracy Trend:                                                │
│  60% ─── 72% ─── 85%  ↑ improving                               │
│  ████    ██████  █████████                                      │
│                                                                 │
│  Most Reliable Patterns:                                        │
│  · "call" → Call project (94% accuracy)                         │
│  · "build" → Deep Work (89% accuracy)                           │
│  · "Fix" → Delegate prefix (87% accuracy)                       │
│                                                                 │
╰─────────────────────────────────────────────────────────────────╯
```

#### 🔧 Manage Patterns

Use AskUserQuestion to select a pattern, then offer:
- Boost confidence (+5)
- Reset confidence (→ 1)
- Remove pattern

Update via `things_update_pattern` or `things_remove_pattern`.

#### 📜 View History

Read the last 10 entries from `data/history.jsonl` and display:

```
╭─────────────────────────────────────────────────────────────────╮
│  📜 Recent Decisions                                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  10m ago   "Fix garage" → "Delegate: Fix garage"       ✓ kept   │
│  10m ago   "Research AI" → Computer                    ✓ kept   │
│  1h ago    "Build app" → Deep Work                     ✗ changed│
│  1h ago    "Call dentist" → Call                       ✓ kept   │
│                                                                 │
╰─────────────────────────────────────────────────────────────────╯
```

**Time formatting:** Show relative time (10m ago, 1h ago, yesterday, 2d ago).

---

### Option 4: 🎯 Quick Actions

Show quick actions submenu:

```
question: "Quick Action"
header: "Quick"
options:
  - label: "➕ Add Task"
    description: "Create a new task with AI project suggestion"
  - label: "🔍 Search Tasks"
    description: "Find tasks by keyword"
  - label: "✓ Complete Task"
    description: "Mark a task as done"
  - label: "📤 Delegate Task"
    description: "Assign to someone via email"
```

#### ➕ Add Task

Ask for task details:

```
question: "What needs to get done?"
header: "Add"
```

Then:
1. Call `things_suggest_for_task` with the title
2. Show suggestion with confidence
3. Confirm with user
4. Call `things_add_todo` to create

**After creation:**

```
╭───────────────────────────────────────────────────╮
│                                                   │
│  ✓ Added: "[Task Title]"                          │
│                                                   │
│  → [Project Name]                                 │
│                                                   │
╰───────────────────────────────────────────────────╯
```

#### 🔍 Search Tasks

```
question: "Search for?"
header: "Search"
```

Call `things_search` with the query and display results.

#### ✓ Complete Task

Call `things_get_today`, show tasks as options, let user select one to complete.

**After completion, show celebration:**

```
╭───────────────────────────────────────────────────╮
│                                                   │
│  ✓ Done: "[Task Title]"                           │
│                                                   │
│  One down, [N] to go today. Keep rolling!         │
│                                                   │
╰───────────────────────────────────────────────────╯
```

#### 📤 Delegate Task

Show today's tasks, let user select one, then draft delegation email.

---

## Navigation

After any action completes, offer to return to main menu:

```
question: "What's next?"
header: "Nav"
options:
  - label: "↩️ Back to Menu"
    description: "Return to SuperThings hub"
  - label: "👋 Done"
    description: "Exit SuperThings"
```

---

## Execution Flow

1. Print the ASCII banner with rounded corners
2. Determine time of day for greeting
3. Fetch counts in parallel (inbox, today, patterns)
4. Print the dashboard with greeting and counts
5. Show main menu via AskUserQuestion
6. Execute selected action with appropriate empty states or celebrations
7. Offer navigation back to menu or exit

---

## CLI Style Guidelines

- **Rounded corners:** `╭ ╮ ╰ ╯` for all boxes
- **Horizontal/vertical lines:** `│ ─`
- **Section dividers:** `├ ┤`
- **Progress bars:** `████████░░░░`
- **Status indicators:** `✓ ✗ · → ↑`
- **Keep lines under 65 chars** for readability
- **Consistent emoji use** in menu labels
- **Show counts contextually** in descriptions

---

## MCP Tools Reference

| Tool | Purpose |
|------|---------|
| `things_get_inbox` | Get inbox items |
| `things_get_today` | Get today's tasks |
| `things_search` | Search for tasks |
| `things_suggest_for_task` | Get AI suggestion for a title |
| `things_add_todo` | Create a new task |
| `things_update_todo` | Update a task |
| `things_complete_todo` | Complete a task |

**Pattern data lives in:**
- `data/patterns.json` - Learned patterns and stats
- `data/history.jsonl` - Correction history

---

## Example Session

```
$ /superthings

╭───────────────────────────────────────────────────────────────╮
│                                                               │
│    ✓ SuperThings                                              │
│      ─────────────                                            │
│      Intelligent task management that learns from you         │
│                                                               │
╰───────────────────────────────────────────────────────────────╯

╭───────────────────────────────────────────────────────────────╮
│                                                               │
│  Good morning! ☀️  Ready to make today count?                 │
│                                                               │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│    📥 Inbox          📅 Today          🧠 Patterns            │
│   ╭────────╮       ╭────────╮        ╭────────╮              │
│   │   12   │       │   8    │        │   23   │              │
│   ╰────────╯       ╰────────╯        ╰────────╯              │
│                                                               │
╰───────────────────────────────────────────────────────────────╯

? What would you like to do?
  ▶ 📥 Triage Inbox - Sort 12 items into projects · AI suggestions · ~3 min
    ⚡ Get Things Done - Work through Computer & Deep Work tasks
    🧠 Learning System - View patterns · Stats · Manage what I've learned
    🎯 Quick Actions - Add · Search · Complete · Delegate
```
