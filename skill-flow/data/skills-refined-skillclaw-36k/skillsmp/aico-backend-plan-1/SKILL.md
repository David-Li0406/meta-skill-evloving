---
name: aico-backend-plan
description: |
  Create ATOMIC implementation plan for a single backend task. Each step has TDD, exact code, and verification command.

  IMPORTANT: This skill creates MICRO-LEVEL atomic steps, NOT macro architecture plans.
  For architecture planning or feature scoping, use EnterPlanMode instead.

  Use this skill when:
  - Running /backend.plan command
  - User explicitly asks for "atomic steps", "step-by-step plan with verification"
  - Have a specific task from docs/reference/backend/tasks/ and need implementation steps
  - Need granular TDD steps: Types → DB → Test (failing) → Implementation → Test (passing) → API

  DO NOT use for:
  - Architecture planning (use EnterPlanMode)
  - General development planning
  - Feature scoping or estimation

  Output: Present plan to user (not saved to file), each step includes Files, Action, and Verify command.
---

# Plan

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

1. **Read task**: Get details from `docs/reference/backend/tasks/{story}.md`
2. **Read constraints**: Load `docs/reference/backend/constraints.md`
3. **Break into atomic steps** following this order:
   - Types/interfaces first
   - Database migrations
   - Failing tests (TDD)
   - Implementation to pass tests
   - API routes
   - Verification
4. **Keep steps atomic**: One action per step
5. **Present plan to user** (do not save to file)

## Plan Format

````markdown
# [Task Name] - Implementation Plan

> Project: [project-name]
> Created: YYYY-MM-DD
> Task: [task description]
> Estimated steps: N

## Step 1: [Action]

**Files**:

- Create: `src/types/user.ts`

**Action**:
[Exact code]

**Verify**:

```bash
npx tsc --noEmit
```
````

Expected: No errors

```

## Step Order

| Order | Step Type | Purpose |
|-------|-----------|---------|
| 1 | Types | Define interfaces and DTOs |
| 2 | Database | Create migrations |
| 3 | Test (RED) | Write failing test |
| 4 | Implement (GREEN) | Write code to pass test |
| 5 | API | Add routes |
| 6 | Commit | Stage and commit |

## Step Granularity

| Good Steps | Bad Steps |
|------------|-----------|
| Create type file with interface | Create entire model with methods |
| Write one failing test | Write all tests |
| Implement single method | Implement entire service |
| Add one route | Add all routes |

## Key Rules

- ALWAYS write failing test before implementation (TDD)
- MUST include verification command for each step
- ALWAYS follow order: Types → DB → Test → Impl → API
- NEVER combine multiple actions into one step

## Common Mistakes

- ❌ Steps too large → ✅ One action per step
- ❌ Skip verification → ✅ Every step has verify command
- ❌ Implementation before test → ✅ TDD: test first
- ❌ Vague actions → ✅ Include exact code
```
