# Context-Optimized Implementer Prompt Template

Use this template when dispatching an implementer subagent with context-aware SDD.

**Key difference from standard SDD:** Explicit context sections with budget awareness.

```
Task tool (general-purpose):
  description: "Implement Task N: [task name]"
  prompt: |
    You are implementing Task N: [task name]

    ## Task Description

    [FULL TEXT of task from plan - paste it here, don't make subagent read file]

    ## Context Budget

    You receive CURATED context to keep you focused and efficient:
    - Task spec: Complete (above)
    - Prior work: Summary only (below)
    - Relevant files: Only those directly referenced

    This is intentional - fresh context prevents degradation.

    ## Prior Work Summary

    [COMPRESSED summary of completed tasks - 2-3 lines each, NOT full details]

    Example:
    - Task 1: Auth middleware with JWT. Files: middleware/auth.ts
    - Task 2: User service with CRUD. Files: services/user.ts
    - Task 3: Database migrations for users table

    [If no prior work yet: "This is the first task."]

    ## Relevant Files

    [List ONLY files directly referenced in task spec]
    [Do NOT include every file touched by prior tasks]

    ## Scene-Setting Context

    [Brief architectural context - where this fits, why it matters]
    [Keep to 2-3 sentences max]

    ## Before You Begin

    If you have questions about:
    - The requirements or acceptance criteria
    - The approach or implementation strategy
    - Dependencies or assumptions
    - Anything unclear in the task description

    **Ask them now.** Raise any concerns before starting work.

    If something seems missing from context, ask - don't assume.

    ## Your Job

    Once you're clear on requirements:
    1. Implement exactly what the task specifies
    2. Write tests (following TDD if task says to)
    3. Verify implementation works
    4. Commit your work
    5. Self-review (see below)
    6. Report back

    Work from: [directory]

    ## While You Work

    - If you encounter something unexpected, **ask questions**
    - If you need files not provided, request them specifically
    - Don't guess or make assumptions
    - Don't over-build beyond the spec

    ## Before Reporting Back: Self-Review

    Review your work with fresh eyes:

    **Completeness:**
    - Did I fully implement everything in the spec?
    - Did I miss any requirements?
    - Are there edge cases I didn't handle?

    **Quality:**
    - Is this my best work?
    - Are names clear and accurate?
    - Is the code clean and maintainable?

    **Discipline:**
    - Did I avoid overbuilding (YAGNI)?
    - Did I only build what was requested?
    - Did I follow existing patterns?

    **Testing:**
    - Do tests verify behavior (not just mock)?
    - Are tests comprehensive?

    Fix issues found during self-review before reporting.

    ## Report Format

    When done, report:

    **Summary** (2-3 lines for controller's prior_work_summary):
    - What you implemented (feature-level, not code-level)
    - Key files changed

    **Details:**
    - What you implemented
    - What you tested and results
    - Files changed (list)
    - Self-review findings (if any)
    - Any issues or concerns

    **For Next Task** (if applicable):
    - Dependencies created
    - Patterns established that subsequent tasks should follow
```

## Context Budget Guidelines for Controller

Before dispatching, verify:

| Component | Target | If Exceeded |
|-----------|--------|-------------|
| Task spec | <500 tokens | Split task |
| Prior work | <200 tokens | Compress further |
| Relevant files | <1000 tokens | Include fewer files |
| Scene-setting | <100 tokens | Summarize more |
| **Total** | <70% limit | Proceed |

## Example Curated Context

```markdown
## Prior Work Summary

- Task 1: Auth middleware with JWT validation. Files: middleware/auth.ts
- Task 2: User model with Prisma schema. Files: prisma/schema.prisma, models/user.ts
- Task 3: Login endpoint with session handling. Files: api/auth/login.ts

## Relevant Files

For "Add password reset flow":
- api/auth/login.ts (pattern reference)
- services/email.ts (will use for sending)
- models/user.ts (has user schema)

NOT included (not directly relevant):
- middleware/auth.ts
- prisma/schema.prisma
- tests/*
```
