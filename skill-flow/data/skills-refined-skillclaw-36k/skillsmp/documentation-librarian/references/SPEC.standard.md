# SPEC.standard.md — Specification / RFC Standard

## Purpose

A SPEC (or RFC) is a **technical contract**: what the system must do, constraints, invariants, and the design decisions required to implement it.

## Audience

* Engineers implementing or reviewing changes
* Future maintainers
* Stakeholders needing technical guarantees

## Source of truth

* The spec itself (for intended design)
* ADRs (for decision rationale)
* Reference (for finalized public API/config, if applicable)

## Required sections (recommended order)

1. **Title**
2. **Context**

   * why this exists, the problem, current state
3. **Goals**
4. **Non-goals**
5. **Definitions**

   * key terms and scope boundaries
6. **Proposed design**

   * architecture overview + major components
7. **Data model / Interfaces**

   * schemas, types, endpoints, events (as applicable)
8. **Behavior**

   * key flows, edge cases, error handling
9. **Invariants**

   * properties that must always hold true
10. **Security & privacy**
11. **Performance & scalability**
12. **Migration / rollout plan**
13. **Risks**
14. **Open questions**
15. **Acceptance criteria**

* testable conditions for “done”

## Allowed content

* Diagrams, tables, examples
* Alternatives (brief) if ADR doesn’t exist yet

## Forbidden content

* Step-by-step tutorials (Guides)
* Operational incident steps (Playbooks)
* Historical narrative edits (ADRs)

## Maintenance rules

* Changes must be explicit and reviewable.
* Prefer adding clarifying sections over rewriting.
* If the spec is outdated, either:

  * update it (incremental), or
  * mark it as **Superseded** with a link to the replacement.

## Quality checklist

* Goals/non-goals are sharp.
* Acceptance criteria are testable.
* Invariants are stated and enforceable.
* Edge cases and failure modes are addressed.

## Common failure modes

* Spec reads like a blog post
* Missing non-goals → scope creep
* No acceptance criteria → endless debate
