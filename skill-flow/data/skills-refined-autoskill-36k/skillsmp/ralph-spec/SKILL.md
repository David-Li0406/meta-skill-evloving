---
name: ralph-spec
description: Write Ralph specification documents - structured feature specs with clear requirements, acceptance criteria, and implementation guidance for autonomous task execution
license: MIT
compatibility: opencode
metadata:
  category: planning
  system: ralph
---

# Writing Ralph Specs

Use this skill when creating or improving specification documents for Ralph, the autonomous task execution system. Ralph specs drive automated implementation through **construct mode**, which runs a staged loop: INVESTIGATE -> BUILD -> VERIFY (with DECOMPOSE for failures).

## What Makes a Good Ralph Spec

A Ralph spec must be **machine-actionable**. An LLM agent will read this spec and autonomously implement it. Every requirement must be:

1. **Unambiguous** - No room for interpretation
2. **Verifiable** - Clear pass/fail criteria
3. **Atomic** - Decomposable into single-iteration tasks
4. **Complete** - All edge cases and constraints specified

## Spec File Location

Place specs in: `ralph/specs/<spec-name>.md`

Use kebab-case for filenames (e.g., `user-authentication.md`, `api-rate-limiting.md`).

## Required Sections

Every Ralph spec MUST have these sections in order:

### 1. Title (H1)

```markdown
# Feature Name
```

Short, descriptive name. This becomes the spec identifier.

### 2. Overview

```markdown
## Overview

One paragraph explaining WHAT this feature does and WHY it exists.
Focus on the problem being solved, not implementation details.
```

### 3. Requirements

```markdown
## Requirements

### Subsection Name

Detailed requirements organized by topic. Use:
- Bullet points for lists of requirements
- Code blocks for formats, schemas, examples
- Tables for structured data (field definitions, command references)
```

### 4. Acceptance Criteria

```markdown
## Acceptance Criteria

- [ ] Criterion 1: Specific, testable requirement
- [ ] Criterion 2: Another testable requirement
- [ ] Criterion 3: Edge case handling
```

**CRITICAL**: This section drives VERIFY stage. Each criterion becomes a verification check.

## Optional Sections

Add these when relevant:

### Architecture (for complex features)

```markdown
## Architecture

Use ASCII diagrams for flows:

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  Input  │────>│ Process │────>│ Output  │
└─────────┘     └─────────┘     └─────────┘
```

Explain component relationships and data flow.
```

### CLI Commands (for tools)

```markdown
## CLI Commands

| Command | Output | Description |
|---------|--------|-------------|
| `tool cmd` | JSON | Does X |
| `tool cmd --flag` | String | Does Y |
```

### Configuration (for configurable features)

```markdown
## Configuration

```jsonl
{"field": "value", "description": "what it does"}
```

| Field | Default | Description |
|-------|---------|-------------|
| `field` | `value` | What it controls |
```

### Error Handling

```markdown
## Error Handling

| Error Condition | Response |
|-----------------|----------|
| Invalid input | Return error code X |
| Resource not found | Log warning, continue |
```

## Writing Style Rules

### DO

- Use imperative mood: "Add X", "Create Y", "Return Z"
- Be specific: "Return JSON with fields `id`, `name`, `status`"
- Include examples for complex formats
- Specify exact error messages and codes
- Define all acronyms on first use
- Use tables for structured information
- Include edge cases explicitly

### DON'T

- Use vague language: "should be fast", "handle errors appropriately"
- Leave behavior undefined: "returns appropriate response"
- Assume context: always state dependencies explicitly
- Use pronouns without clear antecedents
- Mix requirements with implementation notes
- Include TODOs or "TBD" items - resolve before finalizing

## Acceptance Criteria Best Practices

Each criterion should be:

```markdown
- [ ] [Component] [Action] [Condition] [Expected Result]
```

**Good Examples:**

```markdown
- [ ] `ralph query` returns JSON with `tasks` array containing all pending tasks
- [ ] `ralph task add "desc"` creates task with auto-generated ID matching `t-[a-z0-9]{4}`
- [ ] Build fails gracefully when spec file not found (exit code 1, error message to stderr)
- [ ] Timeout kills long-running task after `timeout_ms` milliseconds and sets `kill_reason: "timeout"`
```

**Bad Examples:**

```markdown
- [ ] System works correctly  <!-- Too vague -->
- [ ] Performance is acceptable  <!-- Not measurable -->
- [ ] Errors are handled  <!-- No specific behavior -->
- [ ] Tests pass  <!-- Which tests? What constitutes passing? -->
```

## Handling Complexity

### Large Features

Break into multiple specs with clear boundaries:

```
ralph/specs/
  auth-core.md        # Core authentication logic
  auth-oauth.md       # OAuth provider integration
  auth-sessions.md    # Session management
```

Reference related specs: "See `auth-core.md` for base authentication flow."

### Dependencies

State dependencies explicitly at the top of Requirements:

```markdown
## Requirements

**Dependencies:**
- Requires `auth-core.md` to be implemented
- Assumes `libfoo >= 2.0` is available

### Feature Requirements
...
```

### Phased Implementation

Use acceptance criteria groupings:

```markdown
## Acceptance Criteria

### Phase 1: Core
- [ ] Basic functionality works
- [ ] Happy path tested

### Phase 2: Edge Cases  
- [ ] Error handling complete
- [ ] All edge cases covered

### Phase 3: Polish
- [ ] Performance optimized
- [ ] Documentation complete
```

## Example: Minimal Spec

```markdown
# Widget Counter

## Overview

Track widget creation and deletion counts per user for billing purposes.

## Requirements

### Data Model

Store counts in `widget_counts` table:

| Column | Type | Description |
|--------|------|-------------|
| `user_id` | UUID | User identifier |
| `created` | INT | Widgets created |
| `deleted` | INT | Widgets deleted |

### API

`GET /api/users/{id}/widget-count`

Returns:
```json
{"user_id": "...", "created": 0, "deleted": 0, "net": 0}
```

`net` = `created` - `deleted`

### Constraints

- Counts must never go negative
- Updates must be atomic (no lost increments under concurrency)

## Acceptance Criteria

- [ ] `widget_counts` table created with correct schema
- [ ] `GET /api/users/{id}/widget-count` returns JSON with all fields
- [ ] Creating widget increments `created` count
- [ ] Deleting widget increments `deleted` count
- [ ] Concurrent updates don't lose increments (test with 100 parallel requests)
- [ ] Attempting to decrement below 0 returns 400 error
```

## Example: Complex Spec (Abbreviated)

```markdown
# Construct Mode

## Overview

Construct mode is Ralph's autonomous execution mode for implementing specs...

## Architecture

```
┌──────────────┐
│   CONSTRUCT  │
│   MODE ENTRY │
└──────┬───────┘
       v
┌──────────────────────────────────────┐
│            ITERATION N               │
│  INVESTIGATE -> BUILD -> VERIFY      │
│       │           │          │       │
│       v           v          v       │
│  [FAILURE?]──> DECOMPOSE ──> NEXT    │
└──────────────────────────────────────┘
```

## Requirements

### Stage: INVESTIGATE
...

### Stage: BUILD
...

### Stage: VERIFY
...

### Stage: DECOMPOSE
...

### Failure Conditions

| Condition | Trigger | Response |
|-----------|---------|----------|
| Timeout | Stage exceeds `timeout_ms` | Kill, decompose |
| Context | Usage > 95% | Kill, decompose |

## CLI Commands

| Command | Description |
|---------|-------------|
| `ralph construct [spec]` | Enter construct mode |
| `ralph query stage` | Get current stage |

## Configuration

| Field | Default | Description |
|-------|---------|-------------|
| `timeout_ms` | 300000 | Max time per stage |
| `max_iterations` | 10 | Iteration limit |

## Acceptance Criteria

### Core Flow
- [ ] Three-phase iteration: INVESTIGATE -> BUILD -> VERIFY
- [ ] BUILD processes tasks in priority order
- [ ] VERIFY accepts or rejects each done task
...

### Failure Handling
- [ ] Timeout triggers DECOMPOSE stage
- [ ] Context limit triggers DECOMPOSE stage
...
```

## Verification Checklist

Before finalizing a spec, verify:

1. **Completeness**
   - [ ] All requirements have acceptance criteria
   - [ ] All edge cases are specified
   - [ ] All error conditions are defined

2. **Clarity**
   - [ ] No ambiguous language
   - [ ] All terms defined
   - [ ] Examples provided for complex formats

3. **Testability**
   - [ ] Each criterion is pass/fail verifiable
   - [ ] Test commands/methods are specified where relevant
   - [ ] Expected outputs are exact, not approximate

4. **Structure**
   - [ ] Required sections present
   - [ ] Logical organization
   - [ ] Consistent formatting

5. **Scope**
   - [ ] Single coherent feature
   - [ ] Dependencies explicitly stated
   - [ ] No circular dependencies with other specs
   - [ ] No task-level circular dependencies (code tasks don't require tests that depend on that code)

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| "Handle errors gracefully" | Undefined behavior | Specify exact error responses |
| "Should be performant" | Not measurable | "Responds within 100ms for 99th percentile" |
| "Similar to X" | Requires inference | Spell out the behavior explicitly |
| Missing edge cases | Incomplete spec | Add explicit criteria for: empty input, max limits, concurrent access, partial failures |
| "etc." or "and so on" | Incomplete list | List all items explicitly |
| Implementation details in Overview | Wrong section | Move to Requirements or Architecture |
| Test requirements in code task acceptance | Circular dependency | Use import verification OR bundle test with code task |

## Avoiding Task-Level Circular Dependencies

**CRITICAL**: When Ralph generates tasks from a spec, acceptance criteria that reference tests can create unfulfillable dependencies.

### The Anti-Pattern

If your spec implies this task structure:

```
Task A: "Extract foo.py"
  accept: "test_foo.py passes"
  
Task B: "Write test_foo.py"  
  deps: [Task A]  # Can't write tests until code exists
```

Task A can never pass verification because:
1. Task A's acceptance requires test_foo.py to pass
2. test_foo.py doesn't exist yet (it's Task B)
3. Task B depends on Task A completing first
4. **Deadlock**: Task A rejected forever

### Solutions

**Option 1: Import-only acceptance for code tasks**

Acceptance criteria for extraction/implementation tasks should verify the code works, not that tests pass:

```markdown
## Acceptance Criteria
- [ ] `from mymodule.foo import FooClass, foo_helper` works
- [ ] `FooClass().process()` returns expected result for basic input
```

Keep test requirements in separate test-focused criteria:

```markdown
- [ ] `pytest tests/unit/test_foo.py` passes
```

Ralph will generate separate tasks, and the test task will naturally depend on the code task.

**Option 2: Bundle code + test in one task**

If you want tests written alongside code, make it explicit in the same criterion:

```markdown
- [ ] `foo.py` implements FooClass with `process()` method AND `test_foo.py` covers basic functionality
```

This creates a single task that includes both.

**Option 3: Test-first with stubs**

Write tests first against a stub/interface:

```markdown
- [ ] `test_foo.py` exists with tests against FooInterface
- [ ] `foo.py` implements FooInterface; all tests pass
```

### Verification Patterns That Work

| Pattern | Acceptance Criteria | Why It Works |
|---------|--------------------|--------------| 
| Import check | `from X import Y works` | No external dependencies |
| Inline validation | `python -c "from X import Y; assert Y().method() == expected"` | Self-contained |
| Separate test task | Code task: imports work; Test task: pytest passes | Clear dependency order |
| Bundled | `X.py AND test_X.py both complete` | Single atomic task |

### Verification Patterns That Fail

| Pattern | Acceptance Criteria | Why It Fails |
|---------|--------------------|--------------| 
| Forward test reference | `test_X.py passes` (when test is separate task) | Test doesn't exist yet |
| Implicit test dependency | `All tests pass` | Unclear scope, may include unwritten tests |
| Cross-task reference | `Works with Y.py` (when Y.py is separate task) | Y.py may not exist yet |

## Integration with Ralph Workflow

Once the spec is written:

1. **Plan**: `ralph plan <spec>` generates tasks from the spec (stored in `ralph/plan.jsonl`)
2. **Construct**: `ralph construct <spec>` enters construct mode, running the staged loop:
   - **INVESTIGATE**: Converts issues into actionable tasks
   - **BUILD**: Executes tasks in priority/dependency order
   - **VERIFY**: Checks done tasks against acceptance criteria, creates new work for gaps
   - **DECOMPOSE**: Breaks down failed tasks that exceeded context/timeout limits
3. **Iterate**: The loop continues until all acceptance criteria are satisfied

### Stage Flow

```
INVESTIGATE -> BUILD -> VERIFY
     ^                    |
     |     [gaps found]   |
     +--------------------+
            
     [failure: timeout/context]
              |
              v
         DECOMPOSE
              |
              v
      (next iteration)
```

The acceptance criteria section is parsed by VERIFY stage - each unchecked item (`- [ ]`) becomes a verification target.

## Tips for Spec Authors

1. **Start with acceptance criteria** - Write what "done" looks like first, then fill in requirements
2. **Use concrete examples** - Show exact inputs and outputs
3. **Think like a verifier** - Can someone unfamiliar with the code check each criterion?
4. **Be explicit about non-requirements** - "This feature does NOT handle X" prevents scope creep
5. **Version your specs** - Major changes should create new spec files
6. **Keep tasks atomic** - Each task should be completable in ONE iteration (< context limit)
7. **Consider context pressure** - Break large features into smaller specs to avoid DECOMPOSE cycles

## Log Files

Ralph logs are stored in `/tmp/ralph-logs/<repo>/<branch>/<spec>/`.

Example: `/tmp/ralph-logs/neo-mittens/main/my-feature/ralph-20260120_162538-build.log`

Logs are organized by:
- **repo**: Repository name (e.g., `neo-mittens`)
- **branch**: Git branch (e.g., `main`, `feature-x`)
- **spec**: Spec name without `.md` extension

Logs are auto-cleared on system restart.

## Ralph CLI Commands Reference

### Planning Commands

| Command | Description |
|---------|-------------|
| `ralph plan <spec>` | Generate tasks from spec (gap analysis). Uses 15min timeout, up to 5 iterations. Clears old tasks/issues for that spec on start. |
| `ralph construct <spec>` | Enter construct mode for spec |
| `ralph query` | Get full current state as JSON |
| `ralph query stage` | Get current stage: INVESTIGATE, BUILD, VERIFY, DECOMPOSE, COMPLETE |

**Plan mode behavior:**
- Prompts to clear/keep existing tasks before starting
- Uses batch `ralph task add '[...]'` for efficiency
- Runs multiple iterations for complex specs
- Minimum 15 minute timeout per iteration

### Task Commands

| Command | Description |
|---------|-------------|
| `ralph task add '<json>'` | Add single task: `{"name": "...", "notes": "...", "accept": "...", "deps": [...]}` |
| `ralph task add '[...]'` | Batch add: `[{"name": "...", ...}, {"name": "...", ...}]` |
| `ralph task done` | Mark current task as done |
| `ralph task accept <id>` | Accept a done task (verification passed) |
| `ralph task reject <id> "reason"` | Reject a done task (add tombstone, retry) |
| `ralph task delete <id>` | Remove a task |
| `ralph task prioritize` | Re-prioritize all pending tasks |

**Batch add example:**
```bash
ralph task add '[
  {"name": "Create config module", "notes": "Create app/ralph/config.py with GlobalConfig...", "accept": "import works"},
  {"name": "Create state module", "notes": "Create app/ralph/state.py...", "accept": "import works", "deps": ["t-xxx"]}
]'
```

Batch add is faster (single save) and supports intra-batch dependencies.

### Issue Commands

| Command | Description |
|---------|-------------|
| `ralph issue add "desc"` | Add an issue for INVESTIGATE stage |
| `ralph issue done` | Remove first issue |
| `ralph issue done-all` | Clear all issues |
| `ralph issue done-ids <id1> <id2> ...` | Clear specific issues |

### Task Relationships

Tasks can have relationships for traceability:

| Field | Set By | Purpose |
|-------|--------|---------|
| `parent` | DECOMPOSE | Links subtask to original oversized task |
| `created_from` | INVESTIGATE | Links task to originating issue |
| `supersedes` | Manual | Links new approach to rejected task |
| `deps` | PLAN/manual | Specifies execution dependencies |

Example with relationships:
```bash
ralph task add '{"name": "Fix race in Worker", "notes": "Add mutex", "accept": "TSAN clean", "created_from": "i-abc1", "priority": "high"}'
```

## Context Management

Ralph uses tiered context management to preserve work:

| Threshold | Action |
|-----------|--------|
| 70% | Warning logged, execution continues |
| 85% | Compaction attempted (summarize conversation) |
| 95% | Kill current task, trigger DECOMPOSE |

When writing specs, keep in mind:
- **Large specs cause DECOMPOSE cycles** - Break into smaller focused specs
- **Acceptance criteria should be independently testable** - Each criterion should be verifiable without running the entire system
- **Include test commands** - Make verification concrete: "Run `pytest tests/test_foo.py`"
