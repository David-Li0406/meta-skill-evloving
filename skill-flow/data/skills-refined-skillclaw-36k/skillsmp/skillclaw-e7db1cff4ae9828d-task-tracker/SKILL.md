---
name: task-tracker
description: Use this skill for effective task management in LLM sessions, allowing you to claim, finish, and track tasks collaboratively.
---

# Task Tracker for LLM Sessions

This skill provides a simple ownership-based task tracking system for multi-agent coordination.

## Commands

### $ba ready

Show issues ready to work on (open + not blocked by dependencies).

**Run:**
```bash
ba ready
```

**Output shows:**
- Issue ID, priority (0-4), type, title
- Only open issues with no unfinished blockers
- Sorted by priority

**Use this to:** Pick your next task from the ready queue.

### $ba claim <id>

Take ownership of an issue (moves it to `in_progress`).

**Run:**
```bash
ba claim <id> --session $SESSION_ID
```

**Example:**
```bash
ba claim ab-x7k2 --session $SESSION_ID
```

**Important:**
- Always use `--session $SESSION_ID` to identify yourself.
- Claiming changes status: `open` → `in_progress`.
- Claiming a `closed` issue reopens it automatically.
- Only one agent can own an issue at a time.

**Use this before:** Starting work on any issue.

### $ba mine

Show issues you currently own.

**Run:**
```bash
ba mine --session $SESSION_ID
```

**Output shows:**
- All issues you've claimed in `in_progress` status
- Sorted by priority

**Use this to:** See what you're currently working on.

### $ba finish <id>

Complete an issue (moves it to `closed`).

**Run:**
```bash
ba finish <id>
```

**Example:**
```bash
ba finish ab-x7k2
```

**Requirements:**
- You must be the current owner (claimed it with your session).
- Changes status: `in_progress` → `closed`.

**Use this when:** Work is done and tested.

### $ba release <id>

Release an issue back to the ready queue (abandon work).

**Run:**
```bash
ba release <id>
```

**Requirements:**
- You must be the current owner.
- Changes status: `in_progress` → `open`.

**Use this when:** You can't complete the work or need to switch focus.

### $ba show <id>

Show detailed information about an issue.

**Run:**
```bash
ba show <id>
```

**Output shows:**
- Full details: status, owner, created_at, updated_at
- Description if present
- Labels and priority
- Comments
- Dependencies (blocks, blocked_by)

**Use this to:** Understand issue requirements before claiming.

### $ba list

List all open issues (excludes closed by default).

**Run:**
```bash
ba list              # Open issues only
ba list --all        # Include closed
ba list --status open
ba list --status in_progress
ba list --status closed
```

**Use this to:** Browse available work.