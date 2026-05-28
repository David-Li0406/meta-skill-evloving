---
name: confident-language-guard
description: Use this skill when drafting or updating directives in documentation to maintain cautious and flexible language, avoiding overly confident or absolute statements unless explicitly required.
---

# Confident Language Guard

## Goal

Keep documentation helpful without overstating certainty or locking in fragile guidance. This is a reminder, not an iron-clad rule.

## Core Rules

- Prefer scoped, time-bound statements (e.g., "in this phase", "for the current repo state").
- Replace absolutes (e.g., "always", "never", "must") with softer language unless a hard rule truly exists.
- Use qualifiers when the information could change (e.g., "appears", "likely", "based on current files").
- Separate **recommendations** from **requirements** and label them clearly.
- State assumptions when they affect the guidance.
- Avoid turning personal judgment into policy language.

## Allowed Absolutes (Exceptions)

- Use absolute language only when a requirement is explicit (e.g., system or repo rules).
- If a hard rule exists, cite the source or file when possible.

## Quick Checklist (Docs Pass)

- Does every directive have a clear source or rationale?
- Can any "always/never/must" be softened without losing meaning?
- Are assumptions stated and scoped?
- Are recommendations labeled as such?

## Example Rewrite

- Before: "You must always run full tests before every commit."
- After: "It is generally safer to run the full test suite before committing; skip only when time is constrained or the change is purely textual."

[Codex - 2026-01-12]