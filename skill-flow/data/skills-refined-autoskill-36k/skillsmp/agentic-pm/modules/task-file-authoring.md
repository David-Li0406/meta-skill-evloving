# Module: Task File Authoring (for Agent Engineers)

## Objective

Generate a task file for each backlog item selected for the sprint.

## Canonical task file sections

Use `templates/task-file.template.md`.

## Mandatory inclusions

Every task file MUST include:

1. **Goal** - Clear, concise statement (1-2 sentences)
2. **Non-goals** - Explicit scope boundaries (prevents scope creep)
3. **Deliverables** - List of files to create/modify
4. **Acceptance criteria** - Checkboxes that must ALL be true
5. **Implementation notes** - Detailed HOW guidance with code examples
6. **Integration notes** - What other tasks depend on this
7. **Do/Don't guidelines** - Positive and negative guidance
8. **Stop-and-ask triggers** - When engineer should escalate
9. **Testing expectations** - What tests must be written/verified
10. **PR preparation** - Title format, labels, dependencies
11. **Implementation Summary section** - Blank, engineer-owned

## Guardrail

If acceptance criteria are ambiguous, you **MUST ask the user** before issuing the task file.

## Quality checklist

Before issuing a task file:
- [ ] Goal is unambiguous (one interpretation only)
- [ ] Non-goals explicitly exclude adjacent work
- [ ] Acceptance criteria are binary (pass/fail, no "mostly done")
- [ ] Code examples match project patterns
- [ ] Integration notes reference specific task IDs
- [ ] Testing expectations are specific (not "add tests")

## Anti-patterns to avoid

- Vague acceptance criteria: "UI should look good"
- Missing non-goals: Opens door to scope creep
- No code examples: Engineers will invent patterns
- "Add appropriate tests": Always specify what tests

## Estimation Guidelines

**MANDATORY**: Before estimating any task, consult `.claude/plans/backlog/INDEX.md` → "Estimation Accuracy Analysis" section.

> **Note:** As of 2026-01-03, estimates are in **tokens only**. Self-reported turns/time are deprecated.
> Actual metrics are auto-captured via SubagentStop hook.

> **Token Estimates Target Billable Tokens**
>
> PM estimates (e.g., "~20K tokens") refer to **billable tokens** (output + cache_create),
> NOT total tokens. Total includes cache reads which inflate the number but don't
> represent new work.

### Category Adjustment Factors

Apply these multipliers to your **token estimates** based on historical data:

| Category | Multiplier | Rationale | Data Points |
|----------|------------|-----------|-------------|
| security | × 0.4 | Simple focused fixes, avg -65% variance | SPRINT-009 |
| refactor | × 0.5 | Consistently overestimated (-52% avg) | 10+ tasks |
| test | × 0.9 | Usually accurate | SPRINT-009 |
| cleanup | × 0.5 | Similar to refactor, but MUST scan scope first | SPRINT-009 |
| schema | × 1.3 | High variance, add buffer | SPRINT-003 |
| config | × 0.5 | Significantly overestimated | SPRINT-003 |
| service | × 0.5 | SPRINT-014/015 confirmed -31% to -45% avg | SPRINT-014/015 |
| docs | × 5.0 | Iteration can spiral (~100x observed) | SPRINT-015 |
| types | × 1.0 | Usually accurate | SPRINT-015 |
| ipc | × 1.5 | Suspected underestimate | - |
| ui | × 1.0 | TBD - need data | - |

### Estimation Process

1. **Categorize the task** - Determine primary category (schema, refactor, test, etc.)
2. **Scan scope (REQUIRED for cleanup tasks)** - See below
3. **Make initial token estimate** - Based on scope and complexity
4. **Apply adjustment factor** - Multiply by category factor
5. **Add SR Review overhead** - +10-40K depending on complexity
6. **Document estimate** - Include Est. Tokens and Token Cap in task file

### Scope Scanning (REQUIRED for Cleanup Tasks)

**Before estimating ANY cleanup task**, scan the actual scope:

```bash
# Console.log cleanup - count occurrences
grep -r "console\." --include="*.ts" --include="*.tsx" | grep -v node_modules | wc -l

# Commented code cleanup - approximate count
grep -rn "^[[:space:]]*//.*{" --include="*.ts" --include="*.tsx" | grep -v node_modules | wc -l

# Any types cleanup - count occurrences
grep -r ": any" --include="*.ts" --include="*.tsx" | grep -v node_modules | wc -l

# Orphaned files - list candidates
find src -name "*.tsx" -exec basename {} \; | sort | uniq
```

**Document the scan results in the task file:**
```markdown
## Scope Scan (Pre-Implementation)

**Scan Date:** YYYY-MM-DD
**Command:** `grep -r "console\." --include="*.ts" | wc -l`
**Result:** 47 occurrences across 23 files

**Estimate based on scan:**
- ~47 occurrences across 23 files
- Base estimate: ~20K tokens
- Apply cleanup multiplier: × 0.5 = ~10K tokens
```

**Why this matters:** SPRINT-009 showed cleanup estimates were often based on stale audit data. Scanning actual scope prevents surprises.

### Example

```
Initial token estimate: ~40K (refactor task)
Category adjustment: × 0.5 = ~20K
SR Review overhead: +15K
Final estimate: ~35K tokens
Token Cap: 140K (4x upper estimate)
```

## Task file naming

```
.claude/plans/tasks/TASK-<ID>-<slug>.md
```

Example: `TASK-101-type-definitions.md`

## Mid-sprint task updates

If requirements change during a sprint:

1. **Create a decision log entry** documenting the change
2. **Update affected task files** with `[UPDATED <date>]` marker at top
3. **Notify assigned engineers** of the change
4. **Do NOT change acceptance criteria** without user approval
5. **If scope expands**, consider splitting into new task

### Update marker format

```markdown
# Task TASK-XXX: <Title>

> [UPDATED 2024-01-15] Acceptance criteria clarified per Decision #3.
> See decision log for details.

## Goal
...
```

---

## Fixture Task Template Additions

**Purpose:** Prevent CI failures from invalid enum values in fixture data.

**Source:** SPRINT-011 TASK-800 used invalid TransactionStage values (`initial_contact`, `negotiation`, `contract`) that don't exist in the actual type definition.

### Type Verification Checklist (Required for Fixture Tasks)

Before committing fixture data, verify:

- [ ] All enum values match actual TypeScript definitions
- [ ] Import types from source files (do NOT hardcode values)
- [ ] Run `npm run type-check` before committing fixture data
- [ ] File paths to type definitions included in task acceptance criteria

### How to Verify Enum Values

```bash
# Find the type definition
grep -rn "type TransactionStage" --include="*.ts" src/ electron/

# Or check the exact file
cat electron/services/types.ts | grep -A 10 "TransactionStage"

# List all exported types from a file
grep -E "^export (type|interface|enum)" electron/services/types.ts
```

### PM Responsibility

When creating fixture tasks, PM MUST:
1. Include exact enum values in task file (not "use appropriate values")
2. Provide file path to type definition
3. Add `npm run type-check` to acceptance criteria
4. List valid values explicitly when enums have domain-specific meanings

### Example

**Bad task spec:**
> "Use appropriate transaction stages for the test emails"

This invites engineers to guess at values like `initial_contact` or `negotiation` which may not exist.

**Good task spec:**
> "Use TransactionStage values from `electron/services/types.ts`:
> - Valid values: `intro`, `showing`, `offer`, `inspections`, `escrow`, `closing`, `post_closing`
> - Do NOT use: `initial_contact`, `negotiation`, `contract` (these don't exist)"

### When to Include This Checklist

Include the Type Verification Checklist when the task involves:
- Creating test fixtures with domain-specific enums
- Adding mock data with typed fields
- Generating fake data for integration tests
- Any task where the engineer might need to use enum values

### Template Addition for Fixture Tasks

Add this section to task files for fixture creation:

```markdown
## Type Definitions Reference

**Enums used in this task:**

| Type | File | Valid Values |
|------|------|-------------|
| TransactionStage | `electron/services/types.ts` | `intro`, `showing`, `offer`, `inspections`, `escrow`, `closing`, `post_closing` |
| TransactionStatus | `electron/services/types.ts` | `pending`, `active`, `archived` |

**Pre-commit verification:**
- [ ] `npm run type-check` passes with fixture data
- [ ] All enum values verified against source definitions
```

**Reference:** BACKLOG-128

---

## Large Fixture Warning

**Purpose:** Prevent engineers from hitting the 32K output token limit when creating large data fixtures.

**Source:** TASK-801 (SPRINT-011) attempted to output 203 messages directly, hit the token limit, and required a workaround.

### When to Add This Warning

When authoring tasks that involve creating fixtures with many items:

| Fixture Size | PM Action |
|--------------|-----------|
| <20 items | No special handling needed |
| 20-50 items | Consider adding generator note |
| >50 items | **MUST add "USE GENERATOR APPROACH" note** |

### Task File Addition for Large Fixtures

Add this section to task files when fixture size exceeds 50 items:

```markdown
### Large Fixture Note

This task creates >X items. **Use generator approach:**
1. Create TypeScript generator script in `scripts/`
2. Run with `npx ts-node scripts/generateFixtures.ts`
3. Commit generated JSON, delete script

See `.claude/docs/shared/large-fixture-generation.md`
```

### Why This Matters

- Claude's Write tool has a 32,000 token output limit
- 200+ items easily exceeds this limit
- Generator scripts run outside Claude (no limit)
- Provides reproducibility and type safety

**Reference:** BACKLOG-121, `.claude/docs/shared/large-fixture-generation.md`
