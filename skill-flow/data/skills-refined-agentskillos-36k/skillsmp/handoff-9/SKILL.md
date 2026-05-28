---
name: handoff
description: Summarize conversation and hand off to a fresh Claude session. Use when user requests handoff, context is getting long, or before ending a work session. Creates a structured summary and spawns fresh Claude with context preserved.
---

# /handoff - Conversation Handoff

## What This Skill Does

When invoked, this skill guides you through:
1. Summarizing the current conversation
2. Calling `wt handoff` with the summary
3. Spawning a fresh Claude session with context preserved

## When to Use

- User explicitly requests: "handoff", "hand off", "fresh session"
- Context is getting long or compacted
- Before a major context switch
- End of a work session

## Handoff Procedure

**Step 1: Create Summary**

Generate a concise summary in this format:

```
SUMMARY:
- Accomplished: [What was completed this session]
- Decisions: [Key decisions made and rationale]
- Current state: [Where things stand - what's done, what's pending]
- Blockers: [Any issues or blockers discovered]
- Next steps: [What the next session should do]
- Notes: [Anything else the next session should know]
```

**Step 2: Execute Handoff**

Run this command with your summary:

```bash
wt handoff -m "SUMMARY:
- Accomplished: [your content]
- Decisions: [your content]
- Current state: [your content]
- Blockers: [your content]
- Next steps: [your content]
- Notes: [your content]"
```

**Step 3: Confirmation**

After running the command, the current session will terminate and a fresh Claude session will start with access to the handoff context.

## Example

User asks for handoff after working on a feature:

```bash
wt handoff -m "SUMMARY:
- Accomplished: Implemented OAuth login flow with Google provider
- Decisions: Used passport.js for OAuth handling (more community support than alternatives)
- Current state: Login working, logout TODO. Tests passing locally.
- Blockers: None
- Next steps: Implement logout endpoint, add session persistence
- Notes: Google Cloud project creds in .env.local (not committed)"
```

## Important Notes

- **Be thorough but concise** - Include key context the next session needs
- **Include rationale** - Not just what, but why decisions were made
- **List blockers** - Even if resolved, document what was encountered
- **Preserve technical details** - File paths, configs, error messages if relevant
- **The new session reads `~/.config/wt/handoff.md`** - Context is preserved automatically

## What Happens After Handoff

1. Summary + auto-collected context written to `~/.config/wt/handoff.md`
2. Context persisted in "Hub Handoff" bead
3. Current tmux session respawns with fresh Claude
4. New Claude sees handoff prompt and reads context
5. Work continues seamlessly
