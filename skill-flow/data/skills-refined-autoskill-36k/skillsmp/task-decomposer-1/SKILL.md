---
name: task-decomposer
description: >
  This skill should be used when the user asks to "break down this feature",
  "decompose this task", "create task list", "plan implementation steps",
  "identify subtasks", or when planning autonomous execution.
  Converts high-level feature requests into atomic, verifiable tasks with dependencies.
---

# Task Decomposition Skill

Break down feature requests into atomic, verifiable tasks with clear dependencies for parallel execution.

## Core Principles

1. **Atomic Tasks** - Each task completes in one focused session
2. **Clear Boundaries** - Each task modifies a specific set of files
3. **Verifiable** - Each task has explicit "done" criteria
4. **Dependency-Aware** - Mark which tasks depend on others

## Decomposition Process

### Step 1: Understand the Feature

Analyze what the feature needs to accomplish:
- Core functionality required
- User-facing behavior
- Backend/API requirements
- Data model needs

### Step 2: Identify Components

Map the feature to architectural components:

| Component Type | Examples |
|---------------|----------|
| Data models / schemas | Database tables, TypeScript types |
| API endpoints / server functions | REST routes, GraphQL resolvers |
| UI components | React components, pages |
| Business logic / utilities | Helper functions, services |
| Tests | Unit tests, integration tests |

### Step 3: Map Dependencies

Determine execution order based on dependencies:
- Data models are usually independent (can parallelize)
- APIs depend on models
- UI depends on APIs (or can run parallel with mocks)
- Integration tests depend on everything

### Step 4: Create Task List

Format each task with this structure:
```
Task N: [Descriptive Name]
- Depends on: none | [task ids]
- Files: [list of files to create/modify]
- Done when: [specific verification criteria]
- Complexity: S/M/L
```

### Step 4b: Feature List Pattern (REQUIRED)

**CRITICAL: All tasks MUST start as failing and require evidence for completion.**

In addition to the task list, generate a YAML feature list that tracks verification status:

```yaml
features:
  - id: task-001
    description: "Create UserForm component with validation"
    status: failing  # MUST always start as failing
    verification_command: "npm test -- --testPathPattern='UserForm'"
    expected_output: "Tests: X passed, 0 failed"
    evidence_required: true  # MUST be true
    can_be_removed: false    # Prevents premature removal

  - id: task-002
    description: "Add API endpoint for user creation"
    status: failing
    verification_command: "npm test -- --testPathPattern='users.api'"
    expected_output: "Tests: X passed, 0 failed"
    evidence_required: true
    can_be_removed: false
```

**Feature List Rules:**

1. **status: failing** - ALL features MUST start with `status: failing`
   - This ensures test-first development
   - A task cannot be marked complete until verification proves it works

2. **evidence_required: true** - ALL features MUST have this set
   - No task can be marked complete without captured verification output
   - Prevents "I think it works" completions

3. **can_be_removed: false** - Prevents scope reduction
   - Features cannot be removed from the list once added
   - If a feature is genuinely not needed, it must be marked as `skipped` with reason

4. **verification_command** - Executable command that proves the feature works
   - Must be specific (not generic "npm test")
   - Must target only relevant tests

5. **expected_output** - Pattern to match in successful output
   - Used to validate that verification actually passed

Write the feature list to `.claude/plans/features-{timestamp}.yaml` alongside the task plan.

### Step 5: Identify Parallel Groups

Group tasks by execution phase:
```
Group 1 (Parallel): [independent tasks]
Group 2 (Parallel): [tasks depending on Group 1]
Group 3 (Sequential): [tasks with complex dependencies]
```

## Output Location

Write decomposed tasks to the execution plan at `.claude/plans/auto-{timestamp}.md`.

## Complexity Guidelines

| Size | Scope | Time Estimate |
|------|-------|---------------|
| S | Single file, simple logic | < 15 min |
| M | Multiple files, moderate logic | 15-45 min |
| L | Many files, complex logic | > 45 min |

Prefer breaking L tasks into smaller S/M tasks when possible.

## Auto-Detection Patterns (NEW)

Use these patterns to automatically identify parallelizable tasks:

### Independent Task Detection

| Pattern | Example Files | Parallelizable? | Reason |
|---------|---------------|-----------------|--------|
| Different components, same type | sidebar.tsx, header.tsx, footer.tsx | ✅ YES | No imports between them |
| CSS/config files | globals.css, tailwind.config.ts | ✅ YES | Config files are independent |
| Multiple API endpoints | api/users.ts, api/posts.ts, api/comments.ts | ✅ YES | Separate route handlers |
| Multiple data models | models/User.ts, models/Post.ts | ✅ YES | Independent type definitions |
| Utility functions | utils/format.ts, utils/validate.ts | ✅ YES | Pure functions, no state |

### Dependent Task Detection

| Pattern | Example Files | Parallelizable? | Reason |
|---------|---------------|-----------------|--------|
| Component + its test | Button.tsx, Button.test.tsx | ❌ NO | Test imports component |
| API + UI consuming it | api/users.ts, UserList.tsx | ❌ NO | UI imports API |
| Type + consumer | types/user.ts, UserCard.tsx | ❌ NO | Component imports type |
| Base + derived | BaseComponent.tsx, ChildComponent.tsx | ❌ NO | Child extends base |
| Schema + migration | schema.prisma, migration.sql | ❌ NO | Migration uses schema |

### Dependency Detection Rules

1. **Import Analysis**
   ```
   IF File A contains "import ... from './FileB'"
   THEN A depends on B → SEQUENTIAL

   IF no imports between files
   THEN INDEPENDENT → PARALLEL
   ```

2. **Type Dependencies**
   ```
   IF Component uses type from types/foo.ts
   THEN types/foo.ts must be created FIRST
   THEN component can run in parallel with OTHER components using same type
   ```

3. **State Dependencies**
   ```
   IF Component A modifies global state that B reads
   THEN A must complete before B → SEQUENTIAL

   IF Components use independent local state
   THEN INDEPENDENT → PARALLEL
   ```

4. **Layer Dependencies (Common Pattern)**
   ```
   Layer 1: Types/Models     → INDEPENDENT (parallelize)
   Layer 2: API/Services     → Depends on Layer 1
   Layer 3: UI Components    → Depends on Layer 2 (or parallel with mocks)
   Layer 4: Integration Tests → Depends on all
   ```

### Quick Decision Flowchart

```
For each pair of files (A, B):
     │
     ▼
Does A import B or B import A?
     │
     ├── YES → SEQUENTIAL (create dependency edge)
     │
     └── NO → Do they share mutable state?
                   │
                   ├── YES → SEQUENTIAL
                   │
                   └── NO → PARALLEL ✓
```

## Parallelization Threshold

**Automatic parallelization triggers when:**
- `independent_tasks >= 3` (configurable in auto-context.yaml)
- No circular dependencies exist
- Tasks are in same architectural layer

**Skip parallelization when:**
- `independent_tasks < 3` (overhead not worth it)
- All tasks have linear dependencies
- Single-file changes
- Trivial fixes (typos, renames)

## Additional Resources

### Reference Files

For detailed decomposition patterns:
- **`references/decomposition-patterns.md`** - Common patterns for CRUD, auth, dashboards, integrations

### Example Files

Working examples in `examples/`:
- **`example-decomposition.md`** - Complete example: "Add user registration with email verification"

## When NOT to Use This Skill

Do NOT use this skill when:

1. **Single-file changes** - No decomposition needed for trivial tasks
2. **Typo fixes and renames** - Skip for simple refactors
3. **User provides explicit task list** - Trust user's own decomposition
4. **Research/audit tasks** - Use research workflow instead
5. **Documentation-only changes** - Docs don't need complex decomposition

## Quality Standards

1. **ALWAYS** identify dependencies between tasks explicitly
2. **NEVER** create tasks that modify the same files in parallel
3. **ALWAYS** include verification criteria ("Done when...")
4. **ALWAYS** assign complexity (S/M/L) to each task
5. **PRIORITIZE** breaking L-sized tasks into smaller S/M tasks
6. **ALWAYS** write task plan to `.claude/plans/` directory
