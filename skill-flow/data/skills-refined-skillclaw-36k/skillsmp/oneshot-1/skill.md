---
name: oneshot
description: Execute one-off tasks (migrations, refactors, prototypes). Sets up workflow in session.md.
user-invocable: true
---

# Oneshot Skill

Entry point for one-off, ad-hoc tasks that don't repeat.

## Applicability

**Use for:**
- Migrations and data transformations
- Refactoring and code cleanup
- Prototypes and experiments
- Infrastructure changes
- Technical debt cleanup
- One-time fixes and updates

**NOT for:**
- Repeatable features (use feature development workflow instead)
- New user-facing functionality requiring ongoing maintenance
- Features needing comprehensive test coverage and documentation

## Methodology Detection

The oneshot skill detects appropriate workflow based on these signals:

**TDD Methodology Signals:**
- Project has test-first culture
- User mentions "test", "TDD", "red/green"
- Feature requires behavioral verification
- Project is pytest-md or similar

**General Methodology Signals:**
- Infrastructure/migration work
- Refactoring without behavior change
- Prototype/exploration
- Default if TDD signals absent

**Workflow Routing:**
- TDD path: `/design` (TDD mode) → `/plan-tdd` → `/orchestrate` → `/vet` → `/review-analysis`
- General path: `/design` → `/plan-adhoc` → `/orchestrate` → `/vet`

## Workflow Selection

Based on methodology detection, oneshot routes to:

**TDD Workflow** (feature development):
- Design with spike test section
- Plan as TDD cycles (RED/GREEN/REFACTOR)
- Execute via tdd-task agent
- Review process compliance

**General Workflow** (oneshot work):
- Design with implementation details
- Plan as sequential steps
- Execute via quiet-task agent
- Review code quality

## Workflow Documentation

- TDD workflow: See `agent-core/agents/tdd-workflow.md`
- General workflow: See `agent-core/agents/oneshot-workflow.md`

## Execution Flow

### 1. Gate Check: Oneshot vs Feature Development

Assess if this is truly a one-off task:

**Feature development signals:**
- Keywords: "feature", "add support for", "users can now", "implement login"
- Requires ongoing maintenance
- Needs comprehensive tests and user-facing docs
- Will be used repeatedly

**Oneshot signals:**
- Keywords: "migrate", "refactor", "update", "fix legacy", "prototype", "cleanup"
- One-time execution
- May not need comprehensive tests
- Implementation-focused, not user-facing

**If feature development detected:**
```
"This looks like feature development (repeatable functionality requiring ongoing maintenance).

The feature development workflow is not yet implemented. You can:
1. Proceed with oneshot workflow (less emphasis on tests/maintenance)
2. Wait for feature dev tooling (recommended for production features)

Which would you prefer?"
```

**If ambiguous:** Ask clarifying questions about repeatability and maintenance needs.

### 2. Check Session State

Read `agents/session.md`:

**If session has significant pending work (>5 pending tasks) OR >100 lines:**
```
"Session has existing pending work. Should I shelve the current work first?

Current pending tasks:
- [list current pending tasks]

Shelving will archive current work to todo.md and reset session.md.

Proceed with shelve? (y/n)"
```

If user says yes: invoke `/shelve` skill, then continue.

### 3. Assess Job Complexity

Analyze the job and determine complexity level:

**Simple (execute directly):**
- Single file changes
- Obvious implementation
- No architectural decisions
- ≤25 lines of code or single focused change

→ Execute directly, no workflow needed. Update session.md with what was done.

**Moderate (planning needed):**
- Clear requirements
- Straightforward implementation choices
- Multiple files but well-defined scope
- No major architectural decisions

→ Set up workflow: Planning → Execution → Review → Completion

**Complex (design needed):**
- Architectural decisions required
- Multiple valid approaches
- User uncertainty about requirements
- Significant codebase impact

→ Set up workflow: Design → Planning → Execution → Review → Completion

### 4. Set Up Workflow in session.md

Update `agents/session.md` with workflow structure.

**For Moderate complexity:**

```markdown
# Session Handoff: [Date]

**Status:** Oneshot workflow initiated - [one-line job description]

## Current Work

**Job:** [Job description from user]

**Type:** One-off task (oneshot workflow)

**Complexity:** Moderate

## Pending Tasks

### Workflow: [job name]
- [ ] Planning - Create runbook with implementation steps (/plan-adhoc)
- [ ] Execution - Run runbook steps (/orchestrate)
- [ ] Review - Verify changes and identify issues (/vet)
- [ ] Completion - Update documentation, finalize work

## Key Context

[Any important context gathered during assessment]

## Next Steps

Start with Planning stage using /plan-adhoc.
```

**For Complex complexity:**

```markdown
# Session Handoff: [Date]

**Status:** Oneshot workflow initiated - [one-line job description]

## Current Work

**Job:** [Job description from user]

**Type:** One-off task (oneshot workflow)

**Complexity:** Complex (architectural decisions needed)

## Pending Tasks

### Workflow: [job name]
- [ ] Design - Explore architecture and make key decisions (/design - requires Opus)
- [ ] Planning - Create runbook with implementation steps (/plan-adhoc)
- [ ] Execution - Run runbook steps (/orchestrate)
- [ ] Review - Verify changes and identify issues (/vet)
- [ ] Completion - Update documentation, finalize work

## Key Context

[Any important context gathered during assessment, including why design stage is needed]

## Next Steps

Start with Design stage using /design. Switch to Opus model for design work.
```

### 5. Begin First Stage

After setting up workflow in session.md:

**If Simple:** Execute the task directly.

**If Moderate:**
- Mark Planning task as in-progress in session.md
- Invoke `/plan-adhoc` skill to create runbook

**If Complex:**
- Mark Design task as in-progress in session.md
- Check current model - if not Opus, advise: "Design stage requires Opus. Please switch to Opus model and invoke /design."
- If Opus, invoke `/design` skill

## Critical Rules

1. **Always update session.md** - Even for simple tasks, record what was done
2. **Be conservative with shelve** - Only suggest if session truly has competing work
3. **Assess accurately** - Complexity assessment affects workflow efficiency
4. **Model awareness** - Advise model switches when needed (Design = Opus)
5. **Feature dev gate** - Redirect to feature dev workflow if applicable
6. **No scope creep** - Oneshot is for one-off tasks only

## Example Interactions

### Example 1: Simple Task

```
User: /oneshot "fix typo in README"

Agent: Assesses as simple task.
Agent: Executes directly (reads README, fixes typo).
Agent: Updates session.md with completion note.
Agent: "Fixed typo in README. Session.md updated."
```

### Example 2: Moderate Task

```
User: /oneshot "migrate database from SQLite to PostgreSQL"

Agent: Assesses as oneshot (one-time migration).
Agent: Assesses as moderate complexity (clear requirements, multiple steps).
Agent: Checks session.md - clean, no shelve needed.
Agent: Sets up workflow in session.md (Planning → Execution → Review → Completion).
Agent: Marks Planning as in-progress.
Agent: Invokes /plan-adhoc to create migration runbook.
```

### Example 3: Complex Task

```
User: /oneshot "refactor authentication system to support multiple providers"

Agent: Assesses as oneshot (one-time refactor, not new feature).
Agent: Assesses as complex (architectural decisions about provider abstraction).
Agent: Checks session.md - has pending work from previous task.
Agent: "Session has pending work. Shelve current work first? (y/n)"
User: "y"
Agent: Invokes /shelve.
Agent: Sets up workflow in session.md (Design → Planning → Execution → Review → Completion).
Agent: Marks Design as in-progress.
Agent: "Design stage requires Opus. Please switch to Opus model and invoke /design."
```

### Example 4: Feature Dev Redirect

```
User: /oneshot "add user profile page with bio and avatar upload"

Agent: Detects feature development signals (new user-facing functionality, ongoing maintenance).
Agent: "This looks like feature development (repeatable functionality requiring ongoing maintenance).

The feature development workflow is not yet implemented. You can:
1. Proceed with oneshot workflow (less emphasis on tests/maintenance)
2. Wait for feature dev tooling (recommended for production features)

Which would you prefer?"

User: "Proceed with oneshot"
Agent: Continues with complexity assessment and workflow setup.
```

## Integration with Other Skills

- **`/design`** - Invoked for complex tasks requiring architectural decisions
- **`/plan-adhoc`** - Invoked for moderate/complex tasks to create runbook
- **`/orchestrate`** - Invoked during execution stage
- **`/vet`** - Invoked during review stage
- **`/shelve`** - Invoked if session needs reset before starting new work
- **`/handoff`** - Used between stages for session handoff

## Session Continuation

When agent loads session.md and finds oneshot workflow:

1. Read session.md to understand current state
2. Identify in-progress task or first pending task
3. Continue from that point
4. Update task status (mark completed when done, mark next as in-progress)

This enables natural multi-session workflow with model switching.
