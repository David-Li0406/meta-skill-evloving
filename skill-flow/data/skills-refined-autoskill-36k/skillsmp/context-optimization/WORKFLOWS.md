# Efficient Workflows

Workflow patterns for maximizing productivity while managing context effectively.

## Workflow 1: Task Batching

### Principle

Group related operations together instead of interleaving unrelated tasks.

### Anti-Pattern: Scattered Work

```
Turn 1: Read user.ts
Turn 2: Read auth.ts
Turn 3: Edit user.ts
Turn 4: Read config.ts
Turn 5: Edit auth.ts
Turn 6: Read user.ts again  <- Wasted context
Turn 7: Edit config.ts
```

### Pattern: Batched Work

```
Turn 1: Read user.ts, auth.ts, config.ts
Turn 2: Plan all changes
Turn 3: Edit user.ts (all changes)
Turn 4: Edit auth.ts (all changes)
Turn 5: Edit config.ts (all changes)
Turn 6: Verify changes
```

### Batching Guidelines

| Batch Type | When to Use |
|------------|-------------|
| File reads | Before any editing |
| Related edits | Same file, same session |
| Test runs | After completing feature |
| Searches | Before implementation |

### Implementation

```
> Before we make changes, let me read all relevant files:
> - src/models/user.ts
> - src/services/userService.ts
> - src/api/users.ts
> - tests/users.test.ts

[Claude reads all at once]

> Now implement the changes across all these files
```

## Workflow 2: Session Planning

### Pre-Session Checklist

Before starting a significant task:

- [ ] Estimate context budget needed
- [ ] Identify files to read
- [ ] Plan compaction points
- [ ] Decide on delegation candidates
- [ ] Name the session

### Session Blueprint

```
> /rename feature-user-roles

Starting work on user roles feature.

Scope:
- Add role model
- Update user model
- Create role API
- Add role checks

Phase 1: Read & Plan (budget: 30%)
Phase 2: Implement models (compact at 60%)
Phase 3: Implement API (compact at 80%)
Phase 4: Test & polish

Let's start with Phase 1...
```

### Session Templates

#### Quick Fix Session

```
Duration: 15-30 minutes
Context budget: Under 50%

1. Identify issue
2. Read relevant code
3. Implement fix
4. Verify fix
5. Done
```

#### Feature Implementation Session

```
Duration: 1-2 hours
Context budget: 50-80% (with compaction)

1. Explore (delegate to subagent)
2. Plan approach
3. Implement core (compact at 60%)
4. Add tests
5. Polish (compact if needed)
6. Document
```

#### Investigation Session

```
Duration: Variable
Context budget: Managed through delegation

1. Define question
2. Delegate exploration to subagent
3. Review findings
4. Deep dive specific areas
5. Synthesize conclusions
```

## Workflow 3: Checkpoint Pattern

### What Are Checkpoints?

Deliberate moments to capture state before continuing.

### Creating Checkpoints

**Before risky operations:**
```
> Checkpoint: About to refactor authentication.
> Current state:
> - Auth works with JWT
> - Tests passing: 45/45
> - Files to modify: auth.ts, middleware.ts
>
> /compact
```

**After milestones:**
```
> Milestone: User CRUD complete.
> Implemented:
> - POST /users (create)
> - GET /users (list)
> - GET /users/:id (detail)
> - PUT /users/:id (update)
> - DELETE /users/:id (delete)
>
> All tests passing.
> /compact
```

### Checkpoint Checklist

- [ ] State what was accomplished
- [ ] List files modified
- [ ] Note any pending issues
- [ ] Identify next steps
- [ ] Run /compact

### Recovery from Checkpoints

If something goes wrong:

```
> /clear

Recovering from last checkpoint:
- User CRUD was complete and working
- Problem occurred during role implementation
- Need to retry role feature with different approach

Starting from: working user CRUD
```

## Workflow 4: Subagent Exploration

### Exploration Pattern

```
Phase 1: Delegate exploration
> Use a subagent to explore the authentication system:
> - Find all auth-related files
> - Identify the auth flow
> - Note any security mechanisms
> - Report key functions and their purposes

[Subagent explores in separate context]
[Returns concise summary]

Phase 2: Targeted work in main context
> Based on that summary, I'll now read src/auth/middleware.ts
> and implement the changes we need.
```

### Exploration vs Implementation Context

| Activity | Context | Why |
|----------|---------|-----|
| "Find all files using X" | Subagent | Many reads, brief output |
| "Understand the auth flow" | Subagent | Exploration heavy |
| "Implement the new feature" | Main | Need full context |
| "Debug this issue" | Main | Need conversation history |
| "Run and analyze tests" | Subagent | Verbose output |
| "Write the fix" | Main | Need editing context |

### Subagent Types for Workflows

```yaml
# For exploration
---
name: explorer
description: Find and summarize code patterns
tools: Read, Glob, Grep
model: haiku
---

# For test analysis
---
name: test-analyst
description: Run tests and report results
tools: Bash, Read, Glob
model: sonnet
---

# For documentation reading
---
name: doc-reader
description: Read and summarize documentation
tools: Read, Glob
model: haiku
---
```

## Workflow 5: Long-Running Tasks

### The Problem

Tasks exceeding practical context limits:
- Major refactorings
- New feature implementations
- Large-scale migrations
- Multi-day projects

### Multi-Session Architecture

```
Session 1: Architecture (30 min)
├── Explore current state (delegate)
├── Design new approach
├── Document decisions
└── Plan implementation phases

Session 2: Foundation (1-2 hours)
├── Core models/types
├── Basic structure
├── Initial tests
└── /compact at checkpoints

Session 3: Implementation A (1-2 hours)
├── First major component
├── Tests for component
└── /compact at checkpoints

Session 4: Implementation B (1-2 hours)
├── Second major component
├── Integration with A
└── /compact at checkpoints

Session 5: Integration & Polish (1 hour)
├── End-to-end testing
├── Bug fixes
├── Documentation
└── Final review
```

### Session Handoff Pattern

End of session:
```
> Session complete.
>
> Progress:
> - [x] User model with roles
> - [x] Role assignment API
> - [ ] Permission middleware (next session)
> - [ ] Admin UI
>
> Key decisions:
> - Roles stored as JSON array on user
> - Permission checks use middleware
>
> Files to review next session:
> - src/models/user.ts (role field)
> - src/api/roles.ts (assignment endpoints)
>
> /compact
```

Start of next session:
```
> /resume user-roles-feature

Continuing from last session.

Done:
- User model with roles
- Role assignment API

Today's focus:
- Permission middleware
- Integration with routes
```

## Workflow 6: Background Agents

### Using Background Execution

For long-running tasks that don't need immediate results:

```bash
# Start background task
claude -p "Run full test suite and report failures" \
  --allowedTools "Bash,Read" \
  --output-format json \
  > test-results.json &
```

### Background + Main Coordination

```
Main session:
> I've started a background agent running tests.
> While that runs, let's implement the next feature.
> [Work on feature]
> Let me check the background results...
```

### Background Task Candidates

| Task | Reason |
|------|--------|
| Full test suites | Takes time, summary sufficient |
| Code linting | Independent, returns report |
| Documentation generation | Standalone task |
| Dependency analysis | Exploration task |
| Security scanning | Independent analysis |

## Workflow 7: Efficient Communication

### Information Density

**Low density (context-heavy):**
```
> I want to add a new endpoint to the API. The endpoint should be
> for creating new users. It should accept a JSON body with name,
> email, and password. It should validate the input and return
> the created user without the password.
```

**High density (context-efficient):**
```
> Add POST /users endpoint:
> - Input: { name, email, password }
> - Validate all fields
> - Return user (no password)
```

### Structured Requests

**Inefficient:**
```
> Can you look at the code and tell me what you think about
> how we handle authentication?
```

**Efficient:**
```
> Analyze src/auth/:
> 1. Security issues?
> 2. Best practices followed?
> 3. Suggested improvements?
```

### Explicit Context Statements

When resuming or after compaction:
```
> Context: Building REST API for user management
> Stack: Bun + Hono + Drizzle
> Current: Implementing role-based access
> Files: src/api/users.ts, src/middleware/auth.ts
```

## Workflow 8: Recovery Patterns

### Recovering from Confusion

When Claude seems confused:

1. **Check context usage**
   ```
   > /cost
   ```

2. **If high, compact**
   ```
   > /compact
   ```

3. **Restate context clearly**
   ```
   > Let me clarify our current state:
   > - Working on: user authentication
   > - Approach: JWT with refresh tokens
   > - Current file: src/auth/tokens.ts
   > - Issue: refresh token not being validated
   ```

### Recovering from Failed Experiments

```
> /clear

Previous attempt failed. Starting fresh.

What didn't work:
- Approach: Caching in memory
- Problem: Lost on restart

New approach:
- Use Redis for session cache
- Persist to database as backup

Starting implementation...
```

### Recovering from Context Overload

When context is critically full:

```
> /compact

[After compact]

Critical items to remember:
1. Database migration half-complete
2. Users table has new columns
3. Old auth flow still active
4. Next: update auth to use new columns

Continuing from step 4...
```

## Workflow Checklists

### New Feature Workflow

- [ ] Name session `/rename feature-name`
- [ ] State objectives and constraints
- [ ] Explore codebase (delegate if extensive)
- [ ] Plan implementation
- [ ] Implement in phases (compact between)
- [ ] Test each phase
- [ ] Final review
- [ ] Document changes

### Bug Fix Workflow

- [ ] Reproduce and understand bug
- [ ] Identify relevant code
- [ ] Read minimal necessary files
- [ ] Implement fix
- [ ] Verify fix
- [ ] Add regression test
- [ ] Done (usually single session)

### Refactoring Workflow

- [ ] Understand current code (delegate exploration)
- [ ] Design target structure
- [ ] Plan incremental changes
- [ ] Make changes (compact every 2-3 files)
- [ ] Run tests after each change
- [ ] Final verification

### Investigation Workflow

- [ ] Define question clearly
- [ ] Delegate exploration to subagent
- [ ] Review findings
- [ ] Deep dive specific areas (main context)
- [ ] Synthesize conclusions
- [ ] Document findings

## Summary: Efficient Workflow Principles

1. **Batch related operations** - Read together, edit together
2. **Plan sessions** - Know your checkpoints
3. **Delegate exploration** - Use subagents for heavy reading
4. **Create checkpoints** - Capture state before compaction
5. **Communicate efficiently** - High information density
6. **Recover gracefully** - Clear patterns for when things go wrong
7. **Use background agents** - For long-running independent tasks
