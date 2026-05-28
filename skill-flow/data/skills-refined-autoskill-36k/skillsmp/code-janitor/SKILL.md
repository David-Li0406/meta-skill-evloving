---
name: code-janitor
description: "Clean up codebases by removing dead code, simplifying logic, and reducing tech debt; use when asked to refactor for simplicity, delete unused code, or tidy dependencies (trigger keywords: cleanup, refactor, tech debt, simplify, remove unused)."
---

# Code Janitor

## What this skill does
- Eliminates dead code, redundant logic, and unnecessary abstractions.
- Simplifies control flow and reduces tech debt with minimal, safe diffs.

## When to use it
- Trigger phrases: "cleanup", "refactor", "tech debt", "simplify", "remove unused".
- Use when the goal is to reduce complexity or remove unused code safely.

## Step-by-step workflow
1) Identify unused code, dead branches, and duplicate logic; confirm intent.
2) Remove or consolidate with minimal diffs; avoid scope creep.
3) Simplify control flow (flatten conditionals, inline single-use helpers).
4) Prune unused dependencies and redundant config only when safe.
5) Update or remove stale comments and docs tied to removed code.
6) Run focused tests or checks to validate behavior.

## Expected outputs / formatting
- List of removals and simplifications with file references.
- Tests run and any remaining risks.
- Notes on follow-ups if larger refactors are deferred.

## Example prompts
- "Clean up unused code in this module."
- "Simplify this workflow and remove dead branches."
- "Remove unused dependencies and tidy the config."
