---
name: code-simplifier
description: Refactor recently modified code to be clearer and more consistent without changing behavior; follow CLAUDE.md conventions and avoid “clever” one-liners.
compatibility: opencode
metadata:
  audience: engineers
  domain: refactoring
  languages: any
---

# Code Simplifier

## Purpose

Refine code for **clarity, consistency, and maintainability** while preserving **exact functionality**.

This skill improves *how* code is written, **not** *what* it does.

## Default scope

- Refactor **only** code that was **recently modified/touched** in the current session (diff/edited files/lines).
- Expand scope only if the user explicitly requests it.

## Non-negotiables

### Preserve behavior (always)
Do **not** change:
- outputs, side effects, observable performance characteristics that are relied upon, or public APIs
- error behavior (what fails, what returns, user-visible messages/types) unless explicitly requested
- data formats, serialization, ordering, timing semantics (when relevant)

If you can’t be confident behavior is unchanged, **ask** for expected behavior/tests.

### Follow project standards (always)
- If `CLAUDE.md` exists, treat it as the **source of truth**.
- Otherwise, follow repository conventions (lint/format, naming, patterns, directory structure).

## Clarity heuristics (language-agnostic)

Prefer:
- **reducing nesting** (guard clauses / early returns / extracting helpers when it clarifies intent)
- removing **redundant code**, dead code, and unnecessary abstractions
- improving naming to make intent obvious (variables, functions, types)
- keeping functions/components/modules single-purpose
- comments that explain **why** (rationale), not **what** (obvious mechanics)

Hard rule:
- **Avoid nested ternary operators** (or equivalent “dense inline branching” patterns).
  Prefer clear multi-branch constructs (`if/else`, `switch`, pattern matching, or well-named helpers).

## Balance: what *not* to do

Avoid “simplifications” that:
- create clever/dense code that’s harder to read (one-liners, tricky short-circuiting, overly abstracted pipelines)
- over-DRY into abstractions that hide intent
- merge multiple concerns into one function/module
- prioritize fewer lines over maintainability
- reduce debuggability (harder breakpoints/stack traces) without strong reason

## When `CLAUDE.md` specifies language/framework rules

Apply them exactly. Examples of project-standard rules you might see:
- import/module conventions (e.g., ES modules, import sorting, extensions)
- “prefer `function` over arrow functions”
- explicit return types for exported/top-level functions (TypeScript)
- framework component patterns (React/Vue/etc.) and explicit props types
- error handling patterns (“avoid try/catch when possible”, etc.)

Treat these as **conditional**: enforce them only if they are part of the project’s standards.

## Workflow

1. **Identify the refactor target**
   - Use the diff/changed files or user-provided snippet to locate recently modified code.
2. **Read surrounding context**
   - Match nearby patterns and repo conventions.
3. **Refine**
   - Apply small, safe transformations that improve readability and consistency.
4. **Sanity-check behavior preservation**
   - Re-check edge cases, error paths, and types/contracts.
5. **Report**
   - Summarize only changes that affect understanding (not every mechanical edit).

## Output expectations

When producing changes:
- Prefer a **patch/diff** or clearly delimited “before/after” blocks.
- Provide a short **change summary** focused on readability/consistency.
- State that behavior is intended to be unchanged, and note any assumptions + what to verify.

