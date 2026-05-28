---
name: session-handoff
description: Use this skill to capture the current session state and generate a handoff prompt for seamless continuation in a new session, especially when the context window is filling up or before ending a productive session.
---

# Session Handoff

Generate a complete handoff package that allows a new session to resume work seamlessly.

## When to Use

- Context window approaching limit
- Before intentionally ending a productive session
- User requests handoff explicitly
- Complex task needs to span multiple sessions

## Handoff Process

### Step 0: Check Token Budget

Read `.claude/memory/.memory-config.md` for token budget (if it exists):
- `economy`: Session summary ~200-400 tokens (brief, 2-3 sentences)
- `light`: Session summary ~400-700 tokens (concise, 3-5 sentences)
- `standard`: Session summary ~600-1000 tokens (default, 5-8 sentences)
- `detailed`: Session summary ~900-1500 tokens (comprehensive, 8-12 sentences)

If no config exists, use `standard` budget.

### Step 1: Sync Memory First

Before generating the handoff, ensure memory is current:
- Update `active-context.md` with the current state
- Add any new decisions to `decisions/`
- Update `progress.md` with completed/in-progress items
- Create session summary in `sessions/`

**Session file format:** `sessions/YYYY-MM-DD-HHMM.md` or `sessions/YYYY-MM-DD-topic.md`

> **Note:** Include timestamp (HHMM) to avoid overwriting previous same-day sessions. The topic suffix is preferred when a clear topic exists.

```markdown
# Session: [date]

## Summary
Brief summary of what was accomplished.
- economy: 2-3 sentences
- light: 3-5 sentences
- standard: 5-8 sentences (default)
- detailed: 8-12 sentences with comprehensive context

## Work Completed
- [Item 1]
- [Item 2]

## Decisions Made
- ADR-NNN: [title] (if applicable)

## Context for Next Session
- [Key context point]

## Open Questions
- [Question if any]

---
*Session duration: ~[time]*
```

### Step 2: Gather Handoff Context

Collect from conversation and memory:
- **Original goal:** What the user asked for
- **Current task:** What we're actively working on
- **Progress:** What's been completed this session
- **Remaining work:** What still needs to be done
- **Key decisions:** Decisions made this session (reference ADRs if created)
- **Blockers/questions:** Unresolved issues
- **Critical files:** Files being actively modified
- **Recent errors:** Any errors we're debugging

### Step 3: Generate Handoff Prompt

Output a copyable prompt:

~~~markdown
## Handoff Prompt (copy everything below)

```
I'm continuing work on [project-name] from a previous session.

## Original Goal
[What the user originally asked for]

## Session Summary
[2-3 sentence summary]

## Current State
- **Active task:** [Current work]
- **Files in progress:** [List of files]
- **Blockers:** [Any blockers]
- **Next steps:** [What needs to be done next]
```
~~~