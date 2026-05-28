---
name: sync-thinking
description: Update the thinking dashboard after sessions. Scans sessions and updates stats.
allowed-tools: Read, Bash, Edit, Write, Glob, Grep
---

# Sync Thinking Dashboard

Updates the thinking dashboard at `~/obsidian/thinking-dashboard.md` by scanning recent sessions.

## When to Use

- After completing a thinking session
- When user runs `/sync-thinking`
- As part of `/today` daily refresh

## Workflow

### 1. Archive Current Dashboard

Run the archive script to preserve current state before updates:

```bash
~/.claude/scripts/archive-thinking-dashboard.sh
```

### 2. Scan Sessions

Find all sessions and categorize by recency:
- Glob: `~/obsidian/Thinking/Sessions/*.md`
- Parse frontmatter for date, topic, tags
- Group by time period: this week, last 2 weeks, older

### 3. Update Dashboard Sections

Update `~/obsidian/thinking-dashboard.md` with:

**Recent Sessions:**
- This week: list sessions from last 7 days
- Last 2 weeks: list sessions from 8-14 days ago

**Session Stats:**
- Total sessions: X
- Sessions this week: X
- Sessions this month: X

## Dashboard Template

```markdown
---
tags: [dashboard, thinking]
updated: YYYY-MM-DD
---

# Thinking Dashboard

**Last Updated:** YYYY-MM-DD

---

## Recent Sessions

### This Week

### Last 2 Weeks

## Session Stats

- **Total Sessions:** 0
- **This Week:** 0
- **This Month:** 0

---

## Quick Start

**Start a thinking session:**
1. Run thinking-partner agent
2. Describe what you want to think through
3. Session file created automatically

**Continue from previous session:**
1. Run thinking-partner agent
2. Reference the previous session
3. New session links via `continues-from` in frontmatter

**Find related sessions:**
- Use tags like `#thread/topic-name` to group related sessions
- Obsidian backlinks show `continues-from` connections

**After a session:**
Run `/sync-thinking` to update this dashboard.
```

## Output

- Archives previous dashboard state to `~/.thinking-archive/`
- Updates `~/obsidian/thinking-dashboard.md`
- Reports summary: X sessions total, Y this week
