---
name: implementing-tasks
description: Use this skill when you need to execute sprint tasks with production-quality code and comprehensive tests, iteratively addressing audit feedback.
---

# Skill body

## Objective
Implement sprint tasks from `grimoires/loa/sprint.md` with production-grade code and comprehensive tests. Generate a detailed implementation report at `grimoires/loa/a2a/sprint-N/reviewer.md`. Address feedback iteratively until approval from the senior lead and security auditor is obtained.

## Allowed Tools
- Read
- Write
- Edit
- Bash
- Glob
- Grep
- Task
- TaskCreate
- TaskUpdate
- TaskList

## Zone Constraints
This skill operates under **Managed Scaffolding**:

| Zone | Permission | Notes |
|------|------------|-------|
| `.claude/` | NONE | System zone - never suggest edits |
| `grimoires/loa/`, `.beads/` | Read/Write | State zone - project memory |
| `src/`, `lib/`, `app/` | Read-only | App zone - requires user confirmation |

**NEVER** suggest modifications to `.claude/`. Direct users to `.claude/overrides/` or `.loa.config.yaml`.

## Integrity Pre-Check (MANDATORY)
Before ANY operation, verify System Zone integrity:
1. Check config: `yq eval '.integrity_enforcement' .loa.config.yaml`
2. If `strict` and drift detected -> **HALT** and report
3. If `warn` -> Log warning and proceed with caution

## Factual Grounding (MANDATORY)
Before ANY synthesis, planning, or recommendation:
1. **Extract quotes**: Pull word-for-word text from source files
2. **Cite explicitly**: `"[exact quote]" (file.md:L45)`
3. **Flag assumptions**: Prefix ungrounded claims with `[ASSUMPTION]`

**Grounded Example:**
```
The SDD specifies "PostgreSQL 15 with pgvector extension" (sdd.md:L123)
```

**Ungrounded Example:**
```
[ASSUMPTION] The database likely needs connection pooling
```

## Structured Memory Protocol
### On Session Start
1. Read `grimoires/loa/NOTES.md`
2. Restore context from "Session Continuity" section
3. Check for resolved blockers

### During Execution
1. Log decisions to "Decision Log"
2. Add discovered issues to "Technical Debt"
3. Update sub-goal status
4. **Apply Tool Result**