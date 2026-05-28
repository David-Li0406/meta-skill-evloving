---
name: handoff
description: Prepare context handoff for next chat session
disable-model-invocation: true
argument-hint: [optional notes]
allowed-tools: Read, Write, Edit, Bash
---

# Context Handoff Skill

Capture everything from the current session and prepare for seamless continuation in a new chat.

## First-Time Setup

Before first use, create the memory directory and starter files:

```bash
mkdir -p ai/memory && \
  [ -f ai/memory/session-history.md ] || printf '# Session History\n\nCumulative record of session summaries. Append new entries at the bottom.\n\n---\n\n' > ai/memory/session-history.md && \
  [ -f ai/memory/learnings.md ] || printf '# Learnings\n\nAccumulated knowledge about user preferences, project patterns, and insights.\n\n---\n\n' > ai/memory/learnings.md && \
  [ -f ai/memory/decisions.md ] || printf '# Decisions\n\nRecord of key decisions made with rationale.\n\n---\n\n' > ai/memory/decisions.md
```

Run this once per project. Files persist across sessions.

---

## Step 1: Gather Session Intelligence

Capture the following from this conversation:

**Context Summary:**
- What was the user trying to accomplish? (high-level goal)
- What specific task/project were we working on?
- What's the current state? (in progress, blocked, completed phase X)

**Decisions Made:**
- What key decisions were made during this session?
- What approaches did we choose (and why)?
- What did we explicitly decide NOT to do?

**Learnings Captured:**
- What did we learn about the user's preferences?
- What did we learn about the codebase/project?
- What patterns or standards were established?
- Any pain points identified?

**Work Completed:**
- What files were created/modified?
- What was accomplished?
- What's the current state of each item?

**Work Remaining:**
- What's left to do?
- What's the immediate next step?
- Any blockers or dependencies?

**Important Context:**
- User preferences discovered (interaction style, coding style, etc.)
- Project-specific knowledge gained
- Technical decisions and rationale
- Anything the next session MUST know

---

## Step 2: Write to Memory Files

Append to these files with session intelligence:

**`ai/memory/session-history.md`**
```markdown
## [DATE] - Session Summary

**Goal:** [what user was trying to accomplish]
**State:** [in progress / blocked / completed]
**Work Done:** [bullet list]
**Next Step:** [immediate next action]

---
```

**`ai/memory/learnings.md`**
```markdown
## [DATE] - Learnings

- [User preference or project insight]
- [Pattern discovered]
- [Technical knowledge gained]

---
```

**`ai/memory/decisions.md`**
```markdown
## [DATE] - Decisions

| Decision | Rationale | Alternatives Rejected |
|----------|-----------|----------------------|
| [choice] | [why] | [what we didn't do] |

---
```

---

## Step 3: Generate Starter Prompt

Create a comprehensive prompt the user can paste into a new chat:

```markdown
# Session Continuation - [DATE]

## Context
I'm continuing a previous session. Here's everything you need to know:

### Project/Goal
[What we're working on and why]

### Current State
[Where we are right now - what's done, what's in progress]

### Immediate Next Step
[The very next thing to do]

### Key Decisions Made
[Important decisions from previous sessions with brief rationale]

### User Preferences (CRITICAL - Follow These)
[Interaction style, quality expectations, workflow preferences]

### Memory Files to Reference
- `ai/memory/session-history.md` - Latest session state
- `ai/memory/learnings.md` - Accumulated learnings
- `ai/memory/decisions.md` - Decision history

### Important Context
[Anything else critical for continuity]

---

## Resume Instructions

Please read the memory files referenced above, then continue where we left off. The immediate next step is:

**[SPECIFIC NEXT ACTION]**

Treat this as a continuation - no need to re-explain context I've provided. Let's pick up where we left off!
```

---

## Output Format

Provide:

1. **Session Summary** - Brief recap of what happened
2. **Files Updated** - List of memory files written
3. **Starter Prompt** - Complete prompt to paste in new chat
4. **Quick Resume** - One-liner for simple continuation

---

## Usage

Invoke with `/handoff` or `/handoff [optional notes about session focus]`.

The skill captures conversation context, writes to persistent memory files, and generates a starter prompt for seamless continuation.
