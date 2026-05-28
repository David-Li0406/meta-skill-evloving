---
name: code-simplifier
description: Simplify and refine code for clarity, consistency, and maintainability while preserving exact behavior; use after code changes to clean up recently modified sections, align with project standards (e.g., CLAUDE.md, AGENTS.md), and avoid unnecessary complexity.
---

# Code Simplifier

## Workflow

- Identify the recently modified code first (prefer `git diff` or files touched in this session).
- Read project standards (e.g., `CLAUDE.md`, `AGENTS.md`) and follow them strictly.
- Simplify structure and naming without changing behavior.
- Keep scope to the modified sections unless explicitly asked to broaden it.

## Refinement Rules

- Preserve functionality exactly; do not change outputs, side effects, or public APIs.
- Prefer explicit, readable code over clever one-liners.
- Reduce unnecessary nesting and redundancy.
- Avoid nested ternaries; use `if/else` or `switch` for multiple conditions.
- Remove obvious comments that restate code; keep only comments that add real intent.
- Do not merge unrelated concerns into one function.

## Standards to Apply

- Use ES modules with proper import sorting and extensions (if applicable).
- Prefer `function` keyword over arrow functions for top-level functions.
- Add explicit return types for top-level functions (if the language supports them).
- Use explicit React component Props types where applicable.
- Use project error-handling patterns; avoid try/catch unless required.
- Follow project naming conventions and style guides.

## Output Expectations

- Provide concise change descriptions only when changes materially affect understanding.
- If standards conflict, note the conflict and follow the project’s documented rule.
- If no safe simplification is possible, state that clearly.
