# Issue Type Definitions

Reference for branching the planning workflow based on work scope.

---

## Initiative

**Scope:** Strategic (months)
**Question limit:** 5
**Taxonomy:** Full (7 areas)

Coordinates multiple features toward a business goal. Creates high-level plan with feature breakdown.

**Examples:**
- "Authentication Overhaul" → SSO, MFA, session management features
- "Data Export System" → CSV export, API endpoints, scheduling features

**Validation focus:** Scope, Integration, Constraints (strategic concerns)

**SDD requirements:**
- Constitution check: Required
- Pre-impl gates: Required (Simplicity, Anti-Abstraction, Integration-First)
- SDD sections: All included by default (Tech Decisions, API Contract, Data Model)
- Markers: Tracked, must resolve before task-dispatch

---

## Feature

**Scope:** Capability (weeks)
**Question limit:** 5
**Taxonomy:** Full (7 areas)

User-facing value with multiple implementation tasks. Creates detailed plan with task breakdown.

**Examples:**
- "Add CSV Export" → handler, formatter, UI, tests
- "Implement Temporal Joins" → IR node, compiler, tests

**Validation focus:** Behavior, Edge Cases, Integration (capability concerns)

**SDD requirements:**
- Constitution check: Skip (checked at Initiative level if part of one)
- Pre-impl gates: Skip
- SDD sections: Opt-in (3 questions during validation)
- Markers: Tracked, should resolve but non-blocking

---

## Task

**Scope:** Implementation (days)
**Question limit:** 3
**Taxonomy:** Minimal (Scope, Behavior, Integration)

Concrete work item, single deliverable. Creates lightweight plan, mostly tasks.md.

**Examples:**
- "Add CSV export handler to API"
- "Create TemporalJoin IR node type"

**Validation focus:** Behavior, Integration (implementation concerns)

**SDD requirements:**
- Constitution check: Skip
- Pre-impl gates: Skip
- SDD sections: None (KISS principle)
- Markers: Minimal tracking

---

## Exploratory

**Scope:** Unknown
**Question limit:** 3 (to classify)
**Taxonomy:** Minimal until classified

For when the user isn't sure of the scope yet. Gathers context first, then transitions to Initiative/Feature/Task.

**Workflow:**
1. Gather context (read files, understand current state)
2. Ask 3 clarifying questions to understand scope
3. Present classification recommendation
4. User confirms → restart with correct type

**Examples:**
- "Help me improve the auth system" → Could be Initiative or Feature
- "Something's wrong with exports" → Could be Task (bug) or Feature (redesign)

---

## Taxonomy Areas by Type

| Area | Initiative | Feature | Task |
|------|-----------|---------|------|
| Scope | Primary | Primary | Primary |
| Behavior | Secondary | Primary | Primary |
| Data Model | Secondary | Primary | N/A |
| Constraints | Primary | Secondary | N/A |
| Edge Cases | N/A | Primary | N/A |
| Integration | Primary | Primary | Primary |
| Terminology | Secondary | Secondary | N/A |

**Primary:** Always ask if uncovered
**Secondary:** Ask if time permits
**N/A:** Skip for this type

---

## Selection Guidance

**Choose Initiative when:**
- Work spans multiple distinct capabilities
- Timeline is quarterly
- Multiple people may work on different parts
- Business goal requires coordination

**Choose Feature when:**
- Delivering one user-facing capability
- Timeline is sprint-to-sprint
- Tasks are implementation details, not separate features
- Value is clear without breaking it down further

**Choose Task when:**
- Single concrete deliverable
- Can complete in a day or two
- Scope is already well-defined
- Part of an existing Feature

**Choose Exploratory when:**
- Unsure which of the above applies
- Need to understand current state first
- Request is ambiguous or open-ended

---

## SDD Integration Summary

| Aspect | Initiative | Feature | Task |
|--------|-----------|---------|------|
| Constitution check | Required | Skip | Skip |
| Pre-impl gates | All 3 | Skip | Skip |
| Tech Decisions | Auto | Opt-in | Skip |
| API Contract | Auto | Opt-in | Skip |
| Data Model | Auto | Opt-in | Skip |
| Markers blocking | Yes | No | No |
| validation.yaml | Full | Full | Skip |
| dependencies.yaml | Full DAG | Phase-based | Skip |
| context.md | High-level | Standard | Skip |

**Task output = 2 files:** spec.md (lightweight) + tasks.yaml

**Rationale:**
- Initiatives need maximum rigor (strategic, long-running)
- Features balance rigor with velocity (opt-in SDD sections)
- Tasks prioritize speed (KISS, 2 files only)
