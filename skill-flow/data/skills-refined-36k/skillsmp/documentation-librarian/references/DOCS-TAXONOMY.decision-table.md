# DOCS-TAXONOMY.decision-table.md — Document Type Classification Decision Table

## Purpose

This decision table classifies **what kind of document to create or update** based on intent and content signals, to prevent:

* specs turning into guides
* READMEs turning into dumping grounds
* playbooks mixing with architecture
* references drifting into narratives
* roadmaps becoming promises

This is the **type system** for documentation.

---

## How to use (mandatory)

1. Identify the **primary intent** of the change you’re documenting.
2. Find the matching row in the table.
3. Write/update **only** that doc type.
4. If you touch multiple intents, split into multiple docs or use cross-links.
5. If you’re unsure: **stop and consult DEV** (do not guess).

---

## Decision table

### Legend

* ✅ = belongs here
* ❌ = does not belong here
* ⚠️ = only small amounts, and only if it prevents a mistake
* “Primary intent” must be singular.

| Primary intent / question you’re answering                 | Create/Update this doc type | Must include                                              | Must NOT include                             | Typical triggers                                              |
| ---------------------------------------------------------- | --------------------------- | --------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------- |
| “What is this repo and where do I start?”                  | **README**                  | purpose, non-goals, quick start, doc map                  | deep rules, full APIs, incident steps        | new repo, onboarding friction, entry points changed           |
| “How do I do X step-by-step?”                              | **Guide**                   | prerequisites, numbered steps, verification               | contracts, deep rationale, incident response | onboarding, common workflows, usage tasks                     |
| “What must the system do / how is it designed?”            | **SPEC / RFC**              | goals, non-goals, design, invariants, acceptance criteria | tutorials, operational runbooks              | new feature, major behavior change, architectural change      |
| “Why did we choose this approach?”                         | **ADR**                     | context, decision, alternatives, consequences             | full spec, tutorials, procedures             | architecture choice, dependency choice, major tradeoff        |
| “What is the exact interface/schema/config?”               | **Reference**               | exact fields/types, constraints, errors, examples         | narrative, rationale, step-by-step how-to    | API/config surface changes, type schema changes               |
| “How do we operate/respond when X happens?”                | **Playbook**                | triggers, procedure, verification, rollback, escalation   | architectural debate, long tutorials         | incidents, on-call routines, releases, migrations             |
| “What are we doing next and in what order?”                | **Roadmap**                 | horizon, themes, milestone criteria, dependencies, status | promises, fake dates, implementation details | planning cycles, reprioritization, shipped milestones         |
| “What are the guiding rules/invariants of this project?”   | **Principles**              | clear principles, implications, tradeoffs, change policy  | specs/reference details, long narratives     | repeated debates, consistency drift, culture alignment        |
| “What worldview/position are we taking in this domain?”    | **Manifesto**               | thesis, core claims, boundaries, tradeoffs, commitments   | APIs, runbooks, hidden assumptions as facts  | public positioning, domain alignment, philosophy articulation |
| “This file is generated — how do we keep it reproducible?” | **Generated Docs**          | generated notice, source, regen steps, determinism        | hand-written narrative mixed in              | schema-driven docs, auto API docs, changelog generation       |

---

## Tie-breaker rules (when multiple rows seem valid)

Use this strict precedence:

1. **Reference beats Guide** when the content is exact definitions (fields/types/errors).
2. **Playbook beats Guide** when it’s time-sensitive operational action (incidents/rollbacks).
3. **SPEC beats README** when it defines behavior/constraints (README should link to SPEC).
4. **ADR beats SPEC** for “why”; SPEC can reference ADR but should not retell history.
5. **Principles beat Manifesto** when the content is enforceable rules (manifesto is stance).
6. If still ambiguous: **consult DEV**.

---

## Minimal “sanity checks” per type (fast lint)

### README

* Can a new dev start in <10 minutes?
* Does it clearly say what it is *not*?
* Does it link to deeper docs instead of duplicating them?

### Guide

* Are there explicit steps and verification?
* Could someone follow without guessing?

### SPEC

* Are non-goals explicit?
* Are acceptance criteria testable?
* Are invariants stated?

### ADR

* Is status present?
* Are alternatives real and consequences honest?
* Is it append-only (or superseded correctly)?

### Reference

* Is everything exact and constraint-driven?
* Are errors and edge conditions documented?

### Playbook

* Are triggers and rollback explicit?
* Can someone execute without tribal knowledge?

### Roadmap

* Are statuses truthful?
* Are dependencies and risks visible?
* Is it intention, not a promise?

### Principles

* Are principles testable and constraining?
* Are tradeoffs acknowledged?

### Manifesto

* Is the thesis clear in one sentence?
* Do claims lead to concrete commitments?
* Are boundaries explicit?

### Generated docs

* Is regeneration documented and deterministic?
* Is manual editing discouraged/controlled?

---

## Anti-patterns (what to avoid)

* “Everything in README”
* “Guide that quietly defines new behavior” (should be SPEC)
* “Spec that teaches” (should be Guide)
* “Reference that argues” (should be ADR/Principles/Manifesto)
* “Playbook without rollback”
* “Roadmap with dates nobody can defend”
* “ADR rewritten to match current taste”

---

## Output rules for maintainers (Documentation Librarian integration)

* Always classify the change with this table **before** editing.
* In Mode 2B (Relationship Repair), update the **necessary subtree**, but still obey type boundaries.
* If type boundaries conflict across existing docs, prioritize:

  * Reference accuracy
  * Spec correctness
  * Playbook operational safety
  * Then update README/Guides to link correctly
  