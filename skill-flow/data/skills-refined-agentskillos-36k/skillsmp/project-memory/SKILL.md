---
name: project-memory
description: Manages long-term project context, architectural decisions, and known issues. Use this when the user asks about project history, "why" something was done, or before starting a major refactor.
---

# Project Memory System

You are the keeper of this project's long-term memory. Your goal is to ensure we do not repeat mistakes or violate
architectural decisions.

## Memory Files

You manage the following files in the `docs/memory/` directory (create them if they don't exist):

1. `decisions.md`: Records architectural choices (ADRs) and why we made them.
2. `lessons.md`: Records tricky bugs we solved and specific commands that worked.
3. `active-context.md`: A scratchpad for the current "focus" of development.

## Capabilities

### 1. Record a Decision

When the user makes a significant choice (e.g., "Let's use Signals instead of RxJS"), you must:

1. Create/Update `docs/memory/decisions.md`.
2. Add a new entry with: Date, Context, Decision, and Consequences.

### 2. Check Context

Before answering complex architectural questions or starting a refactor, you must:

1. Read `docs/memory/decisions.md` to ensure you aren't violating past rules.
2. Read `docs/memory/lessons.md` to see if we've solved this before.

### 3. Update Lessons

If you fix a difficult bug (especially build errors), automatically append the solution to `lessons.md` so you don't
fail at it next time.