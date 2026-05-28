---
name: nav-marker
description: Use this skill to create context save points that preserve conversation state before breaks, risky changes, or compaction, allowing users to resume work later without re-explaining everything.
---

# Navigator Marker Skill

Create context markers - save points that preserve conversation state so you can resume work later without re-explaining everything.

## When to Invoke

Invoke this skill when the user:
- Says "save my progress", "create checkpoint", "mark this"
- Says "before I take a break", "save before lunch"
- Mentions "risky refactor ahead", "experiment with new approach"
- Says "end of day", "stopping for today"
- Before compacting context

**DO NOT invoke** if:
- User is asking about existing markers (use listing, not creation)
- Context is fresh (< 5 messages exchanged)

## Execution Steps

### Step 1: Check Navigator Structure

Verify `.agent/.context-markers/` directory exists:

```bash
mkdir -p .agent/.context-markers
```

### Step 2: Determine Marker Name

**If user provided name**:
- Use their name (sanitize: lowercase, hyphens for spaces)
- Example: "Before Big Refactor" → "before-big-refactor"

**If no name provided**:
- Auto-generate with timestamp: `marker-{YYYY-MM-DD}-{HHmm}`
- Example: `marker-2025-10-16-1430`

**Ask user for optional note**:
```
Creating marker: [name]

Add a note? (optional - helps remember context later)
Example: "OAuth working, need to add tests"

Note:
```

### Step 3: Generate Marker Content [EXECUTE]

**IMPORTANT**: You MUST actively capture ToM sections (User Intent, Corrections, Belief State).

Create marker document with this structure:

```markdown
# Context Marker: [name]

**Created**: [YYYY-MM-DD HH:MM]
**Note**: [user's note or "No note provided"]

---

## Conversation Summary

[Summarize last 10-15 messages:
- What user was working on
- Key decisions made
- Problems solved
- Current progress state
]

## Documentation Loaded

[List docs that were Read during session:
- Navigator: ✅ .agent/DEVELOPMENT-README.md
- Task: TASK-XX-feature.md
- System: project-architecture.md
- SOPs: [if any]
]

## Files Modified

[List files with Write/Edit calls:
- src/auth/login.ts (implemented OAuth)
- src/routes/auth.ts (added endpoints)
- tests/auth.test.ts (created tests)
]

## Current Focus

[What user is working on right now:
- Feature: Authentication with OAuth
- Phase: Integration complete, testing pending
- Blockers:
```