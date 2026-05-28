---
name: handoff
description: Capture session context before ending for seamless resume by next agent. Use when ending a session, switching contexts, or when user runs /handoff.
---

# /handoff - Session Handoff

Generate a handoff summary to ensure context continuity for the next session.

## Process

1. **Identify the active feature**
   - If argument provided, use that feature: `/handoff <feature-name>`
   - Otherwise, check `specs/` for the most recently modified ledger.md
   - If no specs, summarize the session work generally

2. **Gather session context**
   - What was accomplished this session
   - What's currently in progress or blocked
   - Files modified (check git status if available)
   - Any gotchas or non-obvious context discovered

3. **Update ledger.md**
   - Move completed items to Done
   - Update Next with current pending items
   - Add any new context to the Context section
   - Update Phase and Blocked status

4. **Write handoff summary**

   Append to `specs/<feature>/handoff.md`:

   ```markdown
   ## Session: <date>

   ### Completed
   - <what was done>

   ### In Progress
   - <what's partially done>

   ### Blocked
   - <blockers if any>

   ### Critical Context
   - <things the next session MUST know>

   ### Files Touched
   - <list of modified files>

   ### Resume Command
   <command or instruction to pick up where we left off>
   ```

5. **Confirm** the handoff is complete and ledger.md is updated

## Key Principle

The goal: if a new agent starts the next session and reads only the spec's `AGENTS.md` and `ledger.md`, they can continue effectively without re-discovering context.
