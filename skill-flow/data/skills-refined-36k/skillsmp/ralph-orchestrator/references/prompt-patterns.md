# Prompt Patterns for Ralph Loops

Best practices for writing prompts that lead to successful Ralph loops.

## Core Principles

### 1. Clear Completion Criteria

The most important element of any Ralph prompt is unambiguous completion criteria.

**Bad**:
```
Build a todo API and make it good.
```
- "Good" is subjective
- No way to verify completion
- Claude will guess when to stop

**Good**:
```
Build a REST API for todos.

When complete:
- All CRUD endpoints working (verified by curl commands)
- Input validation in place (invalid data returns 400)
- Tests passing with >80% coverage
- README with API documentation

Output: <promise>COMPLETE</promise>
```
- Each criterion is testable
- Clear verification method
- Explicit completion signal

### 2. Incremental Goals

Break work into phases that build on each other.

**Bad**:
```
Create a complete e-commerce platform with user authentication,
product catalog, shopping cart, checkout, order management,
and admin dashboard.
```
- Too much at once
- No clear starting point
- Easy to lose track of progress

**Good**:
```
Phase 1: Basic Setup
- Initialize project structure
- Add health check endpoint
- Verify: curl localhost:3000/health returns 200

Phase 2: User Model
- Create User table migration
- Add User model with validation
- Verify: tests pass

Phase 3: Authentication
- Add login/register endpoints
- Implement JWT tokens
- Verify: can register and login via API

[Continue with phases...]

Output <promise>COMPLETE</promise> when all phases done.
```
- Each phase is small and focused
- Clear dependencies between phases
- Verification at each step

### 3. Self-Correction Patterns

Build in mechanisms for Claude to catch and fix its own mistakes.

**Pattern: Test-First**
```
For each feature:
1. Write a failing test first
2. Implement until test passes
3. If test fails after implementation, debug
4. Don't proceed until test is green
```

**Pattern: Verification Loops**
```
After implementing each endpoint:
1. Run the test suite
2. If any test fails, fix it before continuing
3. Don't mark endpoint as done until tests pass
```

**Pattern: Checkpoint Commits**
```
After each working feature:
1. Run all tests
2. If green, commit with descriptive message
3. If not, fix before committing
4. Never commit broken code
```

### 4. State Reading Instructions

Since Ralph re-feeds the same prompt, Claude needs explicit instructions to read state.

**Essential Pattern**:
```
## Before Starting Any Work

1. Read progress.md to understand:
   - What iteration you're on
   - What you learned in previous iterations
   - What you're currently working on

2. Read AGENTS.md for:
   - Discovered patterns
   - Architectural decisions
   - Known issues

3. Check git log to see recent commits

DO NOT start working until you've read these files.
```

### 5. Escape Hatch Instructions

Prevent infinite loops by providing clear escape paths.

**Pattern: Attempt Limits**
```
If you've tried the same approach 3 times without success:
1. Document what you tried in progress.md
2. Document the exact error
3. Try ONE different approach
4. If that also fails, mark as BLOCKED and move to next task
```

**Pattern: Skip and Return**
```
If blocked on a dependency:
1. Note the blocker in progress.md
2. Move to a non-dependent task
3. Return to blocked task later
4. If still blocked after other tasks, document for human review
```

---

## Anti-Patterns to Avoid

### 1. Vague Success Criteria

**Avoid**:
- "Make it work well"
- "Good error handling"
- "Proper testing"
- "Clean code"

**Instead use**:
- "Returns 200 for valid requests, 400 for invalid"
- "All thrown errors have error codes and messages"
- "Tests cover happy path and 3 edge cases per endpoint"
- "Passes ESLint with zero warnings"

### 2. No Verification Method

**Avoid**:
```
Add user authentication.
```

**Instead use**:
```
Add user authentication.

Verification:
1. POST /register with {email, password} returns 201 and user object
2. POST /login with valid credentials returns 200 and JWT token
3. GET /protected with valid token returns 200
4. GET /protected without token returns 401
```

### 3. Missing State Instructions

**Avoid**: Assuming Claude remembers previous iterations

**Instead**: Always include explicit state reading instructions at the start of the prompt.

### 4. No Progress Tracking

**Avoid**: Prompts that don't mention updating progress files

**Instead**: Include mandatory progress tracking after each action.

### 5. Infinite Loop Potential

**Avoid**: Prompts with no escape hatches for stuck situations

**Instead**: Always include attempt limits and skip-and-return patterns.

---

## Template Structures

### Simple Task Template

```markdown
# Task: [Name]

## Goal
[1-2 sentence description]

## Success Criteria
When ALL of these are true, output <promise>DONE</promise>:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Before Each Iteration
1. Read progress.md for current state
2. Read AGENTS.md for patterns

## After Each Action
1. Update progress.md with what you learned
2. If pattern discovered, add to AGENTS.md
3. Commit working code

## If Stuck
After 3 attempts on same issue:
1. Document in progress.md
2. Try alternative approach
3. If still stuck, mark as BLOCKED

## Start Here
[Clear first action to take]
```

### Multi-Phase Template

```markdown
# Task: [Name]

## Mission
[Problem statement]

## Phases

### Phase 1: [Name]
- [ ] [Step 1]
- [ ] [Step 2]
Verify: [How to verify phase complete]

### Phase 2: [Name]
- [ ] [Step 1]
- [ ] [Step 2]
Verify: [How to verify phase complete]

[More phases...]

## Completion
When all phases complete, output <promise>ALL PHASES DONE</promise>

## State Management
[State reading and updating instructions]

## Escape Hatches
[What to do if stuck]
```

### Story-Based Template

```markdown
# Task: [Name]

## Stories

### US-001: [Title]
As a [user], I want [feature] so that [benefit]

Acceptance Criteria:
- [ ] [Criterion]
- [ ] [Criterion]

Verify: [Verification method]

### US-002: [Title]
[...]

## Completion
When all stories pass, output <promise>ALL STORIES PASS</promise>

## Workflow
1. Read state files
2. Find first incomplete story
3. Follow TDD: test → implement → verify
4. Update story status when passing
5. Move to next story
6. Repeat until all pass

## Escape Hatches
[...]
```

---

## Prompt Length Considerations

- Keep prompts focused but complete
- Include all necessary instructions (don't assume Claude remembers)
- Reference external files for details (progress.md, AGENTS.md)
- Aim for 500-1500 words in the core prompt
- Use templates to ensure consistency
