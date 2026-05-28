---
name: nestjs
description: Master NestJS coordinator that plans, implements, reviews, and verifies features using parallel sub-tasks, skills, and rules with comprehensive quality validation
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - Skill
  - TodoWrite
  - AskUserQuestion
---

# NestJS

**Purpose:** Master NestJS coordinator that delivers production-ready features through comprehensive planning, parallel execution, and rigorous quality validation.

## When to Use

- Feature implementation requiring multiple steps
- Complex refactoring across multiple files
- Database schema changes with migrations
- Multi-module updates
- Tasks requiring research + implementation + validation

## Capabilities

- Plan-first approach with user approval
- Parallel execution of independent tasks
- Elimination of false positives through double-verification
- Quality gates (lint, typecheck, tests)
- Comprehensive code review

## How to Use

```
/nestjs "Create a product management feature with CRUD operations"
/nestjs "Implement RBAC for user management module"
/nestjs "Refactor authentication to use new auth provider"
```

## Skill Chaining Workflow

This skill automatically chains other skills in a specific sequence:

1. **Implementation Phase** - Uses `api-*` skills to generate code
2. **Review Phase** - Uses `review` skill (multiple iterations if needed)
3. **Fix Phase** - Uses `nestjs` skill again to fix issues
4. **Validation Phase** - Uses `lint-fix`, `test-runner`, `api-nestjs-reviewer`

### Iterative Review Loop

```
[Implementation] → [Review] → Issues Found?
                     ↓              YES
                     └───────→ [Fix] → [Review Again]
                                      ↓
                                   No Issues?
                                      ↓
                                [Quality Gates]
```

**Iteration Rules:**

- Maximum 3 review-fix iterations to prevent infinite loops
- After 3rd iteration, escalate to user for manual intervention
- Each review must be narrower (focus on remaining issues only)

## Process

### PHASE 1: PLANNING

1. Understand requirements thoroughly
2. Research existing patterns using parallel Explore agents:
   ```
   Task('Explore user management patterns', subagent_type='Explore')
   Task('Find CQRS handler examples', subagent_type='Explore')
   Task('Analyze repository patterns', subagent_type='Explore')
   Task('Check auth guard usage', subagent_type='Explore')
   ```
3. Create detailed implementation plan
4. Verify plan against architecture rules
5. **GET USER APPROVAL** before proceeding (use AskUserQuestion if needed)

### PHASE 2: IMPLEMENTATION

1. Execute plan using relevant skills (can run in parallel):
   ```
   Skill('api-feature-cqrs --name=Product --fields="name:string,price:number"')
   Skill('api-data-repository --name=Product --table=products')
   Skill('api-controller --name=Product --operations="create,update,delete"')
   Skill('api-dto --name=Product --fields="name:email,price:number"')
   ```
2. Monitor progress with TodoWrite
3. Handle errors and edge cases

### PHASE 3: VALIDATION (Iterative Review Loop)

Execute this loop with max 3 iterations:

```
ITERATION 1:
├─ Skill('review') - Full comprehensive review
├─ If issues found:
│  ├─ Use Skill('lint-fix') for lint issues
│  └─ Fix confirmed issues manually or with sub-skills
├─ Skill('review') again - Verify fixes
└─ Continue to ITERATION 2 if issues remain

ITERATION 2:
├─ Skill('api-nestjs-reviewer') - NestJS-specific review
├─ Fix any remaining confirmed issues
├─ Skill('review') - Final verification
└─ Continue to ITERATION 3 if issues remain

ITERATION 3 (Last chance):
├─ Skill('review') with specific focus on remaining issues
├─ Attempt final fixes
└─ If issues still remain → ESCALATE TO USER
```

**Review Escalation:**
After 3 iterations with unresolved issues, present:

- List of remaining issues
- Why they couldn't be auto-fixed
- Options for user (manual fix, accept as-is, different approach)

### PHASE 4: QUALITY GATES

All gates must pass before marking complete:

1. **Linting:** `Skill('lint-fix')` then verify with `pnpm nx lint api`
2. **Type Check:** `pnpm nx typecheck api`
3. **Unit Tests:** `pnpm nx test api` or `Skill('test-runner --type=unit')`
4. **Integration Tests:** `pnpm nx e2e api` (if applicable)

## Parallel Execution Rules

### Use Parallel For

- Independent research (different parts of codebase)
- Non-dependent analysis (security + performance + patterns)
- Multi-file generation (commands, queries, events simultaneously)
- Validation tasks (multiple linters/checkers)

### Use Sequential For

- Dependent operations (code must be written before reviewed)
- State changes (build must complete before deployment)
- Shared resources (single file being modified)

## False Positive Elimination

### Research Findings

Before reporting any finding:

1. **File Existence Check** - Verify file actually exists
2. **Pattern Usage Check** - Confirm pattern is actually used (not just defined)
3. **Cross-Reference** - Check against multiple sources
4. **Code Behavior** - Test against actual codebase behavior

### Review Findings

Before fixing any issue:

1. **Double-Verify** - Use review skill again
2. **Check Context** - Ensure fix doesn't break existing functionality
3. **Minimal Changes** - Fix only what's confirmed broken
4. **Re-Review** - Confirm fix resolved the issue

## NestJS Architecture Rules

### CQRS Pattern

- Commands in `commands/` directory
- Queries in `queries/` directory
- Events in `events/` directory
- Handlers decorated with `@CommandHandler()`, `@QueryHandler()`, `@EventHandler()`

### Multi-Tenancy

- All tables have `organization_id` column
- All queries filter by tenant
- Controllers extract tenant from request context
- Cache keys are tenant-prefixed

### Security

- Protected endpoints have guards (`@UseGuards(JwtAuthGuard)`)
- PII fields encrypted at rest
- Audit logging on state changes
- Input validation on all endpoints
- Role-based permissions checked

### Best Practices

- Transactions for multi-step writes
- Proper error handling with specific exceptions
- OpenAPI documentation complete
- OpenTelemetry tracing on handlers
- Cache invalidation on updates

## Available Skills

### Core Skills

- `api-feature-cqrs` - Generate complete CQRS feature
- `api-data-repository` - Generate repository with BaseRepository
- `api-controller` - Generate REST controller with OpenAPI
- `api-dto` - Generate DTOs with validation
- `api-feature-module` - Generate NestJS module

### Infrastructure Skills

- `api-auth-guards` - Generate authentication/authorization
- `api-cache-redis` - Generate Redis cache service
- `api-queue-bullmq` - Generate BullMQ job queues
- `api-event-rabbitmq` - Generate RabbitMQ events
- `api-tracing-otel` - Generate OpenTelemetry instrumentation

### Testing Skills

- `api-test-unit` - Generate unit tests
- `api-test-integration` - Generate integration tests
- `api-test-e2e` - Generate E2E tests
- `test-runner` - Run all tests

### Analysis Skills

- `api-nestjs-reviewer` - Review NestJS code
- `api-test-runner` - Run and analyze tests
- `api-migration-verifier` - Verify database migrations
- `api-openapi-reviewer` - Review API documentation

### Utility Skills

- `lint-fix` - Fix linting issues
- `review` - Comprehensive code review
- `debugger` - Diagnose and fix bugs
- `refactor` - Refactor code

## Completion Criteria

A task is complete ONLY when:

- [ ] User requirements fully met
- [ ] All todos marked completed
- [ ] Code review passes (both skills)
- [ ] Linting passes with no errors
- [ ] Type checking passes
- [ ] All unit tests pass
- [ ] Integration tests pass (if applicable)
- [ ] No confirmed issues remain
- [ ] User is satisfied

## Exit Conditions

**STOP and ask user if:**

- Requirements are unclear
- Multiple valid approaches exist
- User approval needed for plan
- Critical issue found that needs decision
- Unexpected blocking issue

## Related Skills

- `create-feature` - Full-stack feature generation
- `create-crud` - CRUD operations using CQRS
- `orchestrator` - General-purpose task coordination

## Related Standards

- `.claude/rules/orchestrator-parallel-execution.md` - Parallel execution patterns
- `.claude/rules/orchestrator-execution-checklist.md` - Pre/during/post checklists
- `apps/api/CLAUDE.md` - API-specific patterns and conventions
