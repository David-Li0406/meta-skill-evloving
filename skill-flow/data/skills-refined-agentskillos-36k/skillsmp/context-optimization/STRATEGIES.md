# Context Optimization Strategies

Detailed strategies for managing context effectively in Claude Code.

## Strategy 1: Proactive Compaction

### When to Compact

Don't wait for warnings. Compact proactively at these points:

| Trigger | Action |
|---------|--------|
| 70% context usage | Compact before continuing |
| Completed milestone | Compact to preserve progress |
| Before complex operation | Compact to maximize available space |
| Switching sub-tasks | Compact at the boundary |
| After large file reads | Compact if not immediately needed |

### Compaction Timing

**Good Times:**
- Just finished implementing a feature
- About to start a new phase
- After a successful test run
- Before exploring unfamiliar code

**Bad Times:**
- In the middle of a multi-step change
- While debugging (need recent context)
- During active file editing
- When about to reference recent discussion

### Pre-Compaction Ritual

Before running `/compact`:

```
Let me summarize where we are:
- Current task: [what you're working on]
- Key decisions: [important choices made]
- Files modified: [list of changed files]
- Next step: [what comes next]

/compact
```

This ensures critical information survives compression.

## Strategy 2: Strategic Clearing

### When to Clear vs Compact

| Scenario | Recommendation | Why |
|----------|----------------|-----|
| Same project, related task | Compact | Preserve relevant context |
| Same project, unrelated task | Clear | Fresh perspective |
| Different project | Clear | Avoid confusion |
| Debugging old issue | Clear | Don't pollute with old attempts |
| Exploring alternatives | Clear | Clean slate for new approach |

### Clean Break Pattern

When clearing for a fresh start:

```
> /clear

Starting fresh on [project/task].

Context:
- Project: [name/path]
- Goal: [what you want to achieve]
- Constraints: [key limitations]
- Related files: [important locations]
```

### Partial Reset Pattern

Sometimes you want to keep some context manually:

```
> /clear

Continuing work on the authentication system.

From previous session:
- Using JWT tokens with refresh mechanism
- Backend in src/api/auth/
- Frontend in src/components/Auth/
- Database schema already migrated

Now focusing on [new aspect]...
```

## Strategy 3: Task Decomposition

### Breaking Large Tasks

Large tasks consume context quickly. Break them down:

**Monolithic (Problematic):**
```
> Implement complete user management with CRUD, roles, permissions, audit logging, and admin UI
```

**Decomposed (Efficient):**

| Session | Task | Scope |
|---------|------|-------|
| 1 | User CRUD API | Backend only |
| 2 | Role system | Data model + API |
| 3 | Permission checks | Middleware + integration |
| 4 | Audit logging | Cross-cutting concern |
| 5 | Admin UI | Frontend implementation |

### Handoff Between Sessions

End each session with a summary:

```
Session 1 complete.

Implemented:
- User model in src/models/user.ts
- CRUD endpoints in src/api/users.ts
- Tests passing in tests/users.test.ts

Next session:
- Add role model
- Implement role assignment
- Update user queries to include roles

Files to review:
- src/models/user.ts (extend for roles)
- src/db/schema.ts (add roles table)
```

### Task Size Guidelines

| Context Budget | Task Size | Example |
|----------------|-----------|---------|
| Under 30% | Single feature | Add one endpoint |
| 30-50% | Small feature set | Complete CRUD |
| 50-70% | Medium feature | Feature with tests |
| 70%+ | Compact first | Then continue |

## Strategy 4: Subagent Delegation

### Delegation Criteria

Delegate when the task:
- Requires reading many files
- Generates verbose output
- Is exploratory/investigative
- Can be summarized in results
- Is independent of main conversation

### Delegation Patterns

#### Pattern 1: Exploration Delegate

```
> Use a subagent to find all files that import the UserService
> and identify how they use it
```

Returns: Concise summary, not full file contents.

#### Pattern 2: Analysis Delegate

```
> Have a subagent analyze the database schema and report:
> - All tables and their relationships
> - Any circular dependencies
> - Potential normalization issues
```

Returns: Structured analysis.

#### Pattern 3: Test Runner Delegate

```
> Delegate running the test suite to a subagent and report
> only failures with their locations
```

Returns: Pass/fail summary, failure details.

### Creating Efficient Agents

```yaml
---
name: context-efficient-explorer
description: Explore and summarize without context bloat
tools: Read, Glob, Grep
model: haiku
---

You are a code exploration assistant optimized for context efficiency.

Rules:
1. Never quote entire files - summarize key points
2. Report findings in bullet points, not prose
3. Identify patterns across files, not individual details
4. Return actionable insights, not raw data
5. Limit response to essential information

When exploring:
- Use Glob to find files
- Use Grep to identify relevant sections
- Read only necessary portions
- Synthesize findings concisely
```

### Delegation vs Direct Work

| Task Type | Approach | Reason |
|-----------|----------|--------|
| Writing code | Direct | Need full context for quality |
| Reading code | Delegate | Exploration is context-heavy |
| Running tests | Delegate | Output is verbose |
| Making edits | Direct | Need to track changes |
| Searching codebase | Delegate | Many operations |
| Debugging | Direct | Need conversation history |

## Strategy 5: Session Planning

### Pre-Session Planning

Before starting a significant task:

1. **Estimate scope**
   - How many files involved?
   - How much reading required?
   - Expected tool usage?

2. **Plan phases**
   - Natural break points
   - Compaction opportunities
   - Delegation candidates

3. **Set checkpoints**
   - Where to compact
   - What to preserve
   - When to clear

### Session Templates

#### Short Session (Under 50% context)

```
Goal: [single focused task]
Files: [2-5 files]
Duration: 15-30 minutes

1. Implement change
2. Test
3. Done
```

#### Medium Session (50-70% context)

```
Goal: [feature implementation]
Files: [5-15 files]
Duration: 1-2 hours

1. Read relevant code (delegate exploration)
2. Plan implementation
3. Implement (compact at 70%)
4. Test and fix
5. Document
```

#### Long Session (Multiple compactions)

```
Goal: [complex feature]
Files: [15+ files]
Duration: 2+ hours

Phase 1: Architecture (compact after)
- Explore codebase
- Design approach
- Document plan

Phase 2: Implementation (compact at 70%)
- Core implementation
- Unit tests

Phase 3: Integration (compact at 70%)
- Wire up components
- Integration tests

Phase 4: Polish
- Edge cases
- Documentation
- Final review
```

## Strategy 6: Context-Aware Commands

### Efficient File Reading

**Context-heavy:**
```
> Read the entire user service file
```

**Context-light:**
```
> Show me just the createUser function from the user service
```

### Efficient Searching

**Context-heavy:**
```
> Read all test files and find authentication tests
```

**Context-light:**
```
> Grep for "describe.*auth" in the tests directory
```

### Efficient Tool Use

**Verbose output:**
```
> Run npm test and show all output
```

**Focused output:**
```
> Run npm test and summarize: how many passed, failed, and list failures only
```

## Strategy 7: Recovery Patterns

### When Context Gets Polluted

Signs:
- Claude seems confused
- Referencing wrong context
- Mixing up files or concepts
- Giving inconsistent answers

Recovery:

```
> /clear

Fresh start. Here's the accurate context:
- Project: [name]
- What's working: [known good state]
- Current issue: [what you're solving]
- Relevant files: [specific files]
```

### When Claude "Forgets"

If Claude loses important context:

1. **Check if compacted** - Information may be summarized
2. **Restate explicitly** - Don't assume, tell Claude again
3. **Reference files** - "As shown in src/config.ts..."
4. **Consider clearing** - If too polluted, start fresh

### When Stuck in a Loop

If Claude keeps trying the same failed approach:

```
> /clear

Let's try a different approach.

Previous attempts that didn't work:
- [approach 1]: [why it failed]
- [approach 2]: [why it failed]

Let's explore: [new direction]
```

## Anti-Patterns to Avoid

### Context-Wasting Behaviors

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Reading entire files repeatedly | Wastes context | Read once, reference by name |
| Asking for full verbose output | Bloats context | Ask for summaries |
| Interleaving unrelated tasks | Pollutes context | One topic per session |
| Never compacting | Hits ceiling | Proactive compaction |
| Compacting too often | Loses nuance | Only at natural breaks |
| Not planning sessions | Inefficient | Plan before starting |

### Recovery from Anti-Patterns

If you've been wasteful:

1. `/compact` if you can continue
2. `/clear` if too polluted
3. Plan the rest of the task
4. Use subagents for exploration
5. Be more intentional going forward

## Summary: The Context-Efficient Mindset

1. **Treat context as a budget** - Plan how to spend it
2. **Compact proactively** - Don't wait for warnings
3. **Clear decisively** - Fresh starts are powerful
4. **Delegate exploration** - Use subagents for heavy lifting
5. **Break down tasks** - Smaller is more manageable
6. **Plan sessions** - Know your checkpoints
7. **State context explicitly** - Help Claude remember
