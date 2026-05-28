---
name: code-review
description: Perform a thorough code review with Staff Software Engineer rigor, grounded in ticket context and relevant documentation.
---

# Code Review

## Purpose
Perform a thorough code review with Staff Software Engineer rigor, grounded in ticket context and relevant documentation.

## When to use
- You are asked to review a change set, PR, or patch.
- You are asked to "review" a ticket or implementation plan.

## When NOT to use
- The request is to implement changes rather than review them.
- The request is only for high-level product feedback without code context.

## Procedure
1. Set the stance: explicitly adopt the mindset of a Staff Software Engineer (risk-focused, system-level, pragmatic).
2. Review the ticket or ask: if a ticket exists, read it first; otherwise, restate the ask and clarify scope and acceptance criteria.
3. Review relevant documentation before judging code changes: identify and read applicable `docs/` (always include `docs/index.md`, plus area-specific docs like extension APIs, IPC boundaries, or component guides).
4. Perform the code review: prioritize correctness, regressions, security, performance, reliability, and missing tests; include file references and line numbers where possible.
5. Provide findings first (ordered by severity), then open questions/assumptions, then a brief change summary and suggested next steps.

## Rules / Guardrails
- Always ground the review in the ticket/ask and documented architecture.
- Always call out missing tests or verification gaps when relevant.
- Never approve or rubber-stamp without addressing material risks.
- Never ignore doc mismatches; flag or request updates if behavior diverges.

## Examples
### Example: review a ticket implementation
Input:
```
Please review the changes for scaffa-7iq.11
```
Output (abridged):
```
Mindset: Acting as a Staff Software Engineer.
Ticket review: scaffa-7iq.11 acceptance criteria understood.
Docs reviewed: docs/index.md, docs/scaffa_extension_api.md.

Findings:
- src/extension-host/extension-context.ts:42: initialize() returns Promise<GraphSnapshot> but caller expects Promise<void>; potential runtime mismatch.
- src/extension-host/extension-context.ts:78: missing unit coverage for new path; add test in src/extension-host/__tests__/...

Questions/Assumptions:
- Is GraphSnapshot serialization stable across IPC? Docs imply yes, but not verified in tests.

Change summary:
- Updates initialize() typing and adds usage in extension context.

Next steps:
1) Add test coverage for initialize() consumers.
2) Confirm IPC payload size is acceptable for large graphs.
```
