---
name: dev-workflow
description: "REQUIRED workflow for all code changes. MUST load FIRST before planning or implementing features, bugs, refactoring, tests, PRs. Covers full cycle from exploration to pull request. Skip only for: one-off scripts, explanations outside project context."
metadata:
  version: "1.4.0"
---

# Dev Workflow

Engineering standards for humans and LLM agents working in codebases.

## Pre-flight Checklist (Do This FIRST)

> **STOP. Complete this checklist BEFORE any planning or coding.**

- [ ] **Create branch**: `git checkout -b feature/<name>` or `fix/<name>` from main
- [ ] **Set task status**: Mark as "In Progress" (if project uses task tracking)
- [ ] **Read relevant code**: Code is truth; docs may be outdated

Then load the appropriate reference file based on your task type (see Task Router below).

## Relationship with Plan Mode / Planning Tools

If your IDE/agent has a built-in planning mode:

1. **Load this skill BEFORE entering plan mode**
2. **Complete the Pre-flight Checklist first**
3. Use plan mode for technical design, but follow this workflow for process
4. The `exploration → design → implementation` flow applies regardless of planning tools

> Plan mode helps you think. This workflow ensures you don't skip steps.

## When to Load This Skill

**MUST load this skill if the task involves ANY of:**
- Implementing a feature or enhancement
- Fixing a bug
- Writing or modifying tests
- Refactoring existing code
- Preparing a commit or PR
- Reviewing code changes

**Do NOT skip this skill** just because the task seems simple. Even "small" changes benefit from the design-first approach.

## Core Principles

1. **Code is truth** — Read codebase first; docs may be outdated
2. **Design before code** — Define behavior via tests before implementation
3. **Tests are design** — Writing tests = specifying behavior, not just verification
4. **Docs are not optional** — Code + Tests + Docs = Complete commit
5. **Minimal blast radius** — Touch only necessary files; no drive-by refactors

## Priority Stack (When Rules Conflict)

1. **Security** — No secrets exposed, no vulnerabilities
2. **Correctness** — Code does what it's supposed to
3. **Data Integrity** — No data loss or corruption
4. **Availability** — System remains operational
5. **Performance** — Acceptable speed/resource usage
6. **Documentation** — Docs reflect reality
7. **Speed of Delivery** — Ship fast (but not at cost of above)

## Task Router

Load references based on current task. Use `cat <base_directory>/references/<file>` to load.

| Task Type | Reference File |
|-----------|----------------|
| Start new task / understand code | `exploration.md` |
| Design feature / write tests | `design.md` |
| **Fix a bug** | `bugfix.md` |
| Write implementation code | `implementation.md` |
| Prepare commit | `precommit.md` |
| Create or update PR | `pullrequest.md` |
| Refactor (no behavior change) | `design.md` + `refactoring.md` |
| Review code | `review.md` |
| Multiple agents in parallel | `multi-agent.md` |

For tasks spanning multiple phases, load references in sequence.

## Quick Reference

### Commit Format

`type(scope): summary`

Types: `feat` | `fix` | `docs` | `test` | `chore` | `refactor`

### Task System (if project uses task tracking)

**Bug Reporting Flow:**

```
GitHub Issues (external)  →  FUTURE_ROADMAP.md (internal)  →  PR closes issue
      ↓                              ↓                              ↓
 Users report bugs           Maintainer triages,            Agent works from
 & request features          adds to roadmap with GH#       roadmap only
```

- **GitHub Issues** — Entry point for users (bugs, feature requests)
- **Roadmap** (`FUTURE_ROADMAP.md`) — Agent's single source of truth; includes `GH` column linking to issues
- **Design docs** (`docs/DESIGN_REMAINING_ISSUES.md`) — Implementation details for complex tasks
- **Archive** — Completed items moved after merge

**Key rule:** Agents read the roadmap, not GitHub Issues directly. PRs use `Closes #123` to auto-close linked issues.

Status flow: `Pending` → `In Progress` → `In Review` → `Done` → `Archived`

**Roadmap format:**

```
| ID | Priority | Item | Status | GH |
|----|----------|------|--------|-----|
| 1  | P1       | Fix auth bug | In Progress | #123 |
| 2  | P2       | Add feature X | Pending | #45 |
| 3  | P3       | Refactor Y | Pending | — |
```

Priority: `P0` (critical) → `P1` (high) → `P2` (medium) → `P3` (low). GH: `#123` or `—` if internal.

### Typical Task Flow

**For new features:**
1. `exploration.md` — Understand code, confirm scope, set status to In Progress
2. `design.md` — **Define behavior via tests BEFORE coding**
3. `implementation.md` — Write code to make tests pass
4. `precommit.md` — Run tests, update docs, commit
5. `pullrequest.md` — Create PR, self-review, respond to feedback

**For bug fixes:**
1. `exploration.md` — Understand code, locate bug area
2. `bugfix.md` — **Reproduce → Write failing test → Fix → Verify**
3. `precommit.md` — Run tests, update docs/CHANGELOG, commit
4. `pullrequest.md` — Create PR

> **Critical:** Do NOT skip the design/reproduce step. If you find yourself writing code without tests, STOP.
