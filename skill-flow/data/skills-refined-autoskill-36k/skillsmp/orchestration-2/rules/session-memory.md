---
title: Session Memory
impact: MEDIUM
tags: orchestration, memory, sessions
---

# Session Memory

Claude Code now has persistent memory across sessions via hooks.

## How It Works

### ON SESSION START (automatic)
- Hook loads previous session context
- You receive: last session info, pending tasks, state
- Acknowledge and offer to continue

### ON PRE-COMPACT (automatic)
- Hook saves memory BEFORE context is wiped
- Runs synchronously -- blocks until complete
- Critical safety net before /compact

### ON MILESTONES (manual -- orchestrator prompts)
- After major features/implementations
- After significant decisions
- When user requests "save session"

## Saving Memory

Memory is saved in two ways:

1. **Automatic on PreCompact** -- Before any `/compact`, the hook saves current state
2. **Manual at milestones** -- Orchestrator prompts user to save at key moments

```python
# When saving at milestones or user request
Task(subagent_type="session-saver", prompt="Save current session state", run_in_background=False)
```

**No automatic save on exit** -- This avoids notification spam. Trust the milestone saves and PreCompact safety net.

## Memory Locations

```
~/.claude/memory/              <- Global (user-wide)
+-- sessions/                  <- Raw transcripts (auto-saved)
+-- last_session.json          <- Metadata of last session
+-- state.json                 <- Structured state (auto-extracted)
+-- pending.md                 <- Pending tasks (auto-extracted)
+-- decisions.md               <- Decision log (auto-extracted)
+-- last_context.txt           <- Quick context snippet
+-- last_extraction.log        <- Log of background extraction

.claude/memory/                <- Project-specific
+-- state.json                 <- Project state (auto-extracted)
+-- pending.md                 <- Project pending (auto-extracted)
+-- decisions.md               <- Project decisions (auto-extracted)
```

## On Session Start

When you see previous session context in your input:

1. **Acknowledge** -- "Welcome back. Last session you were working on..."
2. **Check pending** -- Review pending.md if present
3. **Offer to continue** -- "Want me to continue with [pending task]?"

---

# Auto-Prompts (Session Save Reminders)

**Proactively prompt users to save session at key moments:**

## WHEN TO PROMPT FOR SESSION SAVE:

1. **MAJOR MILESTONE COMPLETED (IMPORTANT!)**
   - After completing a significant feature or fix
   - "Nice work! Want me to save this checkpoint? Say 'save session' to capture your progress."

2. **SIGNIFICANT DECISIONS MADE**
   - After key architectural or design decisions
   - "We made some important decisions. Good time to 'save session' so they're not lost."

3. **BEFORE /compact**
   - PreCompact hook will auto-save, but remind user:
   - "About to compact. Memory will be saved first automatically -- you're covered."

4. **USER SHOWS EXIT INTENT**
   - When user mentions stopping, break, done for now
   - "Before you go -- want me to save session? Otherwise this context won't persist."

5. **LONG SESSION (30+ min of significant work)**
   - After extended productive periods
   - "We've done a lot. Want to checkpoint with 'save session'?"

## When NOT to Auto-Prompt

- Don't prompt after every small task (annoying)
- Don't prompt if user is clearly in flow state
- Don't prompt multiple times in quick succession
- Check autosave config before prompting

---

# Auto-Save Configuration

Auto-save behavior is controlled per-workspace via config files.

## Config Locations (priority order)

```
1. .claude/autosave.json     <- Workspace-specific (highest priority)
2. ~/.claude/autosave.json   <- Global default (fallback)
```

## Config Schema

```json
{
  "enabled": true,
  "idle_save": true,
  "prompt_after_significant_work": true
}
```

| Setting | Description |
|---------|-------------|
| `enabled` | Master switch. If false, no auto-save behavior. |
| `idle_save` | After work + pause in conversation -> auto-save silently |
| `prompt_after_significant_work` | After big implementation -> prompt "save session?" |

## Toggling Auto-Save via Conversation

Users can control auto-save by speaking naturally:

| User says | Action |
|-----------|--------|
| "turn off auto-save" | Set `enabled: false` in workspace config |
| "turn on auto-save" | Set `enabled: true` in workspace config |
| "disable auto-save prompts" | Set `prompt_after_significant_work: false` |
| "enable silent saves only" | Set `idle_save: true`, `prompt_after_significant_work: false` |
