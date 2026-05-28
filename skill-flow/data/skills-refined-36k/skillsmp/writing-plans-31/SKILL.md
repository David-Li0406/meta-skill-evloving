---
name: writing-plans
description: "Use when planning multi-step tasks. ONLY use in Plan mode (Tab). Updates .opencode/docs/PLANNING.md as a living document. Use for research, decisions, and iteration before Build mode."
allowed-tools: Read Write Edit Glob Grep Bash Task
context: fork
---

# Writing Plans

## Overview

Write implementation plans optimized for agentic execution. Plans should contain everything needed to implement without re-research: key decisions, schemas, code examples, file paths, and test criteria.

**Announce at start:** "I'm using the writing-plans skill to update the implementation plan."

**IMPORTANT: Plan Mode Only**
This skill MUST only be used in **Plan mode** (toggle with Tab). Plan mode is READ-ONLY for code but WRITE-ENABLED for planning documents.

**Save plans to:** `.opencode/docs/PLANNING.md` (single living document per project)

## OpenCode Integration

### Plan Mode Enforcement

**CRITICAL:** Before proceeding, verify you are in Plan mode:
- Plan mode indicator should be visible in the TUI
- If in Build mode, instruct user: "Please switch to Plan mode (Tab) before planning."

When in Plan mode:
- Research codebase, gather context
- Propose architecture verbally
- Iterate based on user feedback
- Update `.opencode/docs/PLANNING.md` with decisions
- DO NOT modify application code

### Transition to Build Mode

When user says "Go ahead" or toggles to Build:

**MANDATORY PRE-COMMIT CHECKLIST (DO NOT SKIP):**

1. **Archive sources** → Move research docs to `.opencode/docs/archive/{date}-{name}.md`
2. **Create sources.md** → Index all sources in `.opencode/docs/archive/sources.md`
3. **Update AGENTS.md** → If planning decisions affect project conventions
4. **Update PLANNING.md** → Mark phases complete, update changelog
5. **Create TodoWrite tasks** → From phases in the plan

⚠️ **CRITICAL:** Steps 1-4 MUST be completed BEFORE committing. Do NOT commit without archiving sources and updating steering documents. This is a hard requirement, not a suggestion.

After checklist is complete:
- Begin implementation (code changes now allowed)

### Living Document Model

Unlike dated plan files, `.opencode/docs/PLANNING.md` is a **living document**:

```bash
# Check for existing plan
ls .opencode/docs/PLANNING.md 2>/dev/null
```

**If plan exists:**
1. Read current plan
2. Identify sections needing updates
3. Update relevant sections in-place
4. Append changelog entry (increment version)
5. Mark completed phases with ✅

**If no plan exists:**
1. Create `.opencode/docs/` directory if needed
2. Create new PLANNING.md with header template
3. Initialize changelog with v1.0

## Plan Document Structure

### File Location

```
project-root/
├── .opencode/
│   └── docs/
│       ├── PLANNING.md          # Living plan document
│       └── archive/
│           ├── sources.md       # Source index
│           └── *.md             # Research documents
```

### Header Template

**Every PLANNING.md MUST start with:**

```markdown
# [Project/Feature Name] Implementation Plan

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

**Sources:** `archive/sources.md` | [SRC-001], [SRC-002]

---
```

## Changelog

Track major plan changes with semantic versioning:

```markdown
## Changelog

| Version | Date | Source | Summary |
|---------|------|--------|---------|
| v1.0 | 2026-01-25 | Plan mode | Initial plan |
| v1.1 | 2026-01-25 | User feedback | Added rate limiting to auth phase |
| v2.0 | 2026-01-26 | SRC-003 | Restructured to microservices |
```

**Source types:**
- `Plan mode` - Created during planning session
- `User feedback` - TUI conversation updates
- `SRC-XXX` - Based on archived research
- `Implementation` - Discovered during build

**Version rules:**
- v1.0 → v1.1: Minor additions/clarifications
- v1.x → v2.0: Major restructure or scope change

## Key Decisions Table

For significant technology choices, include a decision table:

```markdown
## Key Decisions

| Decision | Choice | Rationale | Alternatives Rejected |
|----------|--------|-----------|----------------------|
| [Category] | [Selected option] | [Why this fits] | [Option A (reason)], [Option B (reason)] |

**Sources:** [SRC-001], [SRC-002] - see `archive/sources.md`
```

**When to include:**
- Technology stack choices (database, framework, model)
- Architecture patterns (sync vs async, monolith vs services)
- Significant tradeoffs (cost vs performance)

## Source Document Archiving

⚠️ **MANDATORY:** Never delete source documents. When consolidating research, preserve originals in archive.

**Archive Structure:**
```
.opencode/docs/
├── PLANNING.md                   # Active living plan
└── archive/                      # Source documents (REQUIRED)
    ├── sources.md                # Index with key findings (REQUIRED)
    └── {date}-{description}.md   # Original research docs
```

**Source Index Format (`archive/sources.md`):**
```markdown
# Source Documents

| ID | Title | Type | Date | Key Findings |
|----|-------|------|------|--------------|
| SRC-001 | [Research topic] | research | YYYY-MM-DD | [Key insight 1]; [Key insight 2] |
```

**FAILURE TO ARCHIVE = INCOMPLETE IMPLEMENTATION.** Do not mark phases as complete or commit changes until sources are archived.

## Phase Structure (Agent-Native)

Organize work into phases with clear deliverables and test criteria:

```markdown
## Phase N: [Phase Name]

**Deliverables:**
- [ ] `path/to/file.ts` - Description
- [ ] `path/to/test.ts` - Test coverage

**Schema/Types:** (if applicable)
```typescript
interface Example {
  id: string;
  name: string;
}
```

**Code Example:**
```typescript
export function example(): Example {
  return { id: "1", name: "test" };
}
```

**Test Criteria:**
```bash
npm test -- --grep "example"
# Expected: All tests pass
```

**Commit:** `feat: add example functionality`
```

## What to Include

| Element | Why It Matters |
|---------|----------------|
| Key Decisions table | Prevents re-research |
| Database schemas | Exact SQL/types to execute |
| Code examples | Reference implementations |
| Exact file paths | Know where to create/modify |
| Test commands | Verification criteria |
| Commit messages | Consistent git history |

## What NOT to Include

- Micro-steps like "run test, verify it fails" - agent handles naturally
- Overly granular 2-5 minute human-paced steps
- References to non-existent skills

## Task Granularity

**Right-sized for agents:**
- One phase = one logical unit of work
- Phase contains all files, schemas, examples needed
- Test criteria defines "done"
- Commit message provided

**Example:**
```markdown
## Phase 2: User Authentication

**Deliverables:**
- [ ] `src/auth/service.ts` - Auth service with login/logout
- [ ] `src/auth/middleware.ts` - JWT validation middleware
- [ ] `tests/auth/service.test.ts` - Unit tests

**Test Criteria:** `npm test -- auth` passes

**Commit:** `feat(auth): add authentication service`
```

## Remember

**⚠️ BEFORE COMMITTING - MANDATORY STEPS:**
1. Archive source documents to `.opencode/docs/archive/`
2. Create/update `archive/sources.md` index
3. Update AGENTS.md if conventions changed
4. Mark completed phases with ✅ in PLANNING.md

**Planning requirements:**
- Exact file paths always
- Complete code examples (not "add validation here")
- Test commands with expected output
- Reference skills with `@skills/skill-name`
- Phases map to TodoWrite items
- **Update changelog on major changes**

## AGENTS.md Updates

Planning decisions may establish conventions that should be documented in AGENTS.md. After finalizing a plan, check if updates are needed.

### Find the Relevant AGENTS.md

Search from current directory upward to git root:
```bash
# Find closest AGENTS.md in hierarchy
find . -maxdepth 3 -name "AGENTS.md" -o -name "CLAUDE.md" 2>/dev/null | head -1
```

Hierarchy (most specific wins):
1. `./AGENTS.md` - Current directory
2. `../<parent>/AGENTS.md` - Parent directories
3. Root `AGENTS.md` - Project-wide conventions

### When to Update

Update AGENTS.md if the plan establishes:

| Decision Type | AGENTS.md Section |
|---------------|-------------------|
| New naming conventions | Conventions |
| New file/folder structure | Repository Structure |
| New testing patterns | Testing |
| New tool/command usage | Available Commands |
| New skill conventions | Skill Conventions |
| Architecture patterns | Architecture |

### What to Add

Keep updates minimal and focused:

```markdown
## [Section Name]

### [Convention Name] (added YYYY-MM-DD)

[Brief description of the convention]

**Rationale:** `.opencode/docs/PLANNING.md`
```

### What NOT to Add

- Implementation details (belong in plan, not AGENTS.md)
- Temporary decisions (only permanent conventions)
- Feature-specific logic (belongs in code/docs)

### Example Update

If plan establishes a new API versioning convention:

```markdown
## API Conventions

### Versioning (added 2026-01-25)

All API endpoints use URL path versioning: `/api/v1/`, `/api/v2/`

**Rationale:** `.opencode/docs/PLANNING.md`
```

## Execution

After transitioning to Build mode:

1. Use `TodoWrite` to create tasks from phases
2. Execute phases sequentially
3. Run test criteria after each phase
4. Commit after each phase passes
5. Return to Plan mode if scope changes require plan updates
6. Update `.opencode/docs/PLANNING.md` changelog when phases complete
