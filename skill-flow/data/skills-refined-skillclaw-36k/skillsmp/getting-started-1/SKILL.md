---
name: getting-started
description: This skill is loaded automatically at session start via SessionStart hook. Establishes protocols for finding and using skills, checking skills before tasks, brainstorming before coding, and creating TodoWrite for checklists.
allowed-tools: Read, Skill, TodoWrite, mcp__plugin_serena_serena, mcp__plugin_serena_serena_*
---

# Getting Started with Skills

## Skill Check Protocol

Before starting any task:

1. Scan available skills
2. Ask: "Does any skill match this task type?"
3. If yes: Load skill with Skill tool, announce it, follow it
4. Follow the skill exactly

Skills encode proven patterns that prevent common mistakes.

## When Skills Apply

Skills apply when the task involves:

- Testing (TDD, flaky tests, test quality)
- Debugging (bugs, failures, root cause)
- Planning (brainstorming, writing plans, executing plans)
- Code review (requesting, receiving)
- Git workflows (worktrees, branches, merging)
- Verification (completion claims, fix validation)

If a skill exists for the task type, use it.

## Skill Priority

When multiple skills could apply, use this order:

1. **Process skills first** (brainstorming, debugging) - determine HOW to approach
2. **Implementation skills second** (TDD, architecture) - guide execution
3. **Verification skills last** (verification-before-completion) - confirm results

**Examples:**
- "Let's build X" → brainstorming first, then TDD
- "Fix this bug" → systematic-debugging first, then TDD for the fix
- "Add this feature" → TDD skill (implementation is the process)

## Red Flags

**Watch for these thoughts that indicate skill should be used:**

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "This feels productive" | Undisciplined action wastes time. Skills prevent this. |
| "I can do this quickly without process" | Quick without process = slow with rework. |
| "The skill is overkill for this" | Skills exist because simple things become complex. |
| "I remember how this skill works" | Skills evolve. Load the current version. |

**Any of these thoughts = STOP. Check for applicable skill.**

## Shortcuts That Backfire

| Thought                            | Better Approach                                    |
| ---------------------------------- | -------------------------------------------------- |
| "This is just a simple question"   | Questions are tasks. Check for skills.             |
| "I can check git/files quickly"    | Skills tell HOW to check. Use them.                |
| "This doesn't need a formal skill" | If a skill exists, it exists for a reason.         |
| "I remember this skill"            | Skills evolve. Load the current version.           |
| "The skill is overkill"            | Skills exist because simple things become complex. |

## Skills with Checklists

If a skill contains a checklist, create TodoWrite items for each step.

Mental tracking of checklists leads to skipped steps. TodoWrite makes progress visible.

## Announcing Skill Usage

Before using a skill, announce it:

"I'm using [Skill Name] to [what you're doing]."

Examples:

- "I'm using the brainstorming skill to refine your idea into a design."
- "I'm using the dev-workflow:test-driven-development skill to implement this feature."

## Skill Types

**Rigid skills (follow exactly):** TDD, debugging, verification

- Adapting away the structure defeats the purpose.

**Flexible skills (adapt principles):** Architecture, brainstorming

- Core principles apply; specific steps adapt to context.

## Instructions vs. Workflows

User instructions describe WHAT to do, not HOW.

"Add X", "Fix Y" = the goal, not permission to skip brainstorming, TDD, or verification.

## Summary

1. Scan for relevant skills before starting any task
2. If skill exists: load it, announce it, follow it
3. Checklists require TodoWrite tracking
4. Rigid skills: follow exactly. Flexible skills: adapt principles.

## Reference

See `references/skill-integration.md` for decision tree and skill chains.

---

## Planning Workflows

### Recommended Flow: Plugin Commands

```
/dev-workflow:brainstorm → /dev-workflow:write-plan → /dev-workflow:execute-plan
```

| Feature | Benefit |
|---------|---------|
| Plans persist to `docs/plans/` | Version controlled, reviewable |
| Parallel via `Task(run_in_background)` + `TaskOutput` | Respects task dependencies |
| Task grouping by file overlap | Determines which tasks can run parallel |
| Automatic post-completion | Code review + finish branch enforced |
| Resume capability | Orchestrator tracks progress per group |

### How Parallel Execution Works

The `/dev-workflow:execute-plan` command uses background agents for parallelism:

```
1. Analyze task groups by file dependencies
2. FOR each group (groups execute serially):
   a. Launch tasks in group with Task(run_in_background: true)
   b. Wait for all with TaskOutput(block: true)
   c. Update state: current_task = last task in group
3. Proceed to post-completion actions
```

This approach:
- Preserves plan in `docs/plans/` for version control
- Respects task dependencies (groups are serial, tasks within group are parallel)
- No context leak (task content passed to agents only)
- Accurate progress tracking (state updated after confirmed completion)

### When to Use Native `EnterPlanMode` Directly

Use `EnterPlanMode` without plugin commands when:
- Quick prototyping (plan doesn't need to persist)
- Simple 1-3 task features
- You want Claude to write the plan interactively

For features that need plan persistence, code review, and resume capability, use the plugin commands flow.

---

## Planning Methodology (EnterPlanMode)

When entering plan mode via `EnterPlanMode`, use this methodology:

### When to Use AskUserQuestion

**USE AskUserQuestion for:**
- Multiple valid approaches: "JWT tokens vs session cookies for auth?"
- Technology choices: "Which testing framework: pytest or unittest?"
- Unclear scope: "Should this include admin functionality?"
- Trade-off decisions: "Optimize for speed or maintainability?"

**DO NOT use AskUserQuestion for:**
- Decisions you can make from codebase patterns (follow existing conventions)
- Implementation details covered by TDD (tests define behavior)
- Choices the user already specified in their request

**Format:**
```
AskUserQuestion:
  header: "Auth method"  # max 12 chars
  question: "Which authentication approach?"
  multiSelect: false
  options:
    - label: "JWT tokens (Recommended)"
      description: "Stateless, scalable, matches existing API patterns"
    - label: "Session cookies"
      description: "Simpler, but requires server state"
```

Ask questions BEFORE writing the plan, not during execution.

### Phase 1: Explore

Use the native Explore agent with "very thorough" setting to survey the codebase:

- Similar features and existing patterns
- Integration points and boundaries
- Testing conventions and file locations
- Technology stack and frameworks

For complex features (touching 5+ files), dispatch code-architect in background:
```
Task(subagent_type: 'dev-workflow:code-architect',
     prompt: 'Design architecture for [feature]. Focus: minimal changes.',
     run_in_background: true)
```

Continue exploring while architect works. Retrieve results when ready:
```
TaskOutput(task_id: '<architect-task-id>', block: true)
```

### Phase 2: Design

Apply pragmatic-architecture principles:

| Principle | Rule |
|-----------|------|
| Rule of Three | Abstract only after 3+ occurrences |
| YAGNI | Design for today, not hypothetical futures |
| AHA | Prefer duplication over wrong abstraction |
| Colocation | Keep related code together, ≤3 files per feature |

### Phase 3: Write Plan

Each task MUST be self-contained with explicit TDD instructions (teammates may not have skill context):

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/new.py`
- Modify: `exact/path/to/existing.py:50-75`
- Test: `tests/exact/path/test.py`

**TDD Instructions (MANDATORY - follow exactly):**

1. **Write test FIRST** - Before ANY implementation:
   ```python
   def test_behavior():
       # Arrange
       input_data = {...}
       # Act
       result = function(input_data)
       # Assert
       assert result == expected
   ```

2. **Run test, verify FAILURE:**
   ```bash
   pytest tests/path -v
   ```
   Expected: FAIL (proves test catches missing behavior)

3. **Implement MINIMAL code** - Only enough to pass the test, nothing extra

4. **Run test, verify PASS:**
   ```bash
   pytest tests/path -v
   ```
   Expected: PASS (all tests green)

5. **Commit with conventional format:**
   ```bash
   git add -A && git commit -m "feat(scope): description"
   ```

**Why TDD order matters:** Writing tests after implementation doesn't prove the test catches bugs - it only proves the test matches what was written.
````

### Task Requirements

- Exact file paths (from exploration)
- Complete code snippets (not "add validation")
- Test commands with expected output
- TDD cycle: test → fail → implement → pass → commit

### Parallel Groups

Tasks with NO file overlap execute in parallel (3-5 per group):

| Task Group | Tasks | Rationale |
|------------|-------|-----------|
| Group 1 | 1, 2, 3 | Independent modules, no file overlap |
| Group 2 | 4, 5 | Both touch shared types, must be serial |
| Group 3 | 6, 7, 8 | Independent tests, no file overlap |

### Final Task

Always include "Code Review" as the final task.

### Swarm Execution

Use `ExitPlanMode(launchSwarm: true, teammateCount: N)` to spawn parallel teammates.

**Calculate teammateCount:**
| Independent Groups | teammateCount |
|--------------------|---------------|
| 1-2 groups | 2 |
| 3-4 groups | 3-4 |
| 5+ groups | 5 (max) |

**Execution behavior:**
- Each teammate executes one task following embedded TDD instructions
- Each task = one commit
- Teammates work in parallel where tasks have no file overlap
- Tasks in same group with file overlap run sequentially

### State Persistence (Resume Capability)

**State is managed by TodoWrite.** Tasks are tracked as pending/in_progress/completed in the todo list.

The plan file in `docs/plans/` is the source of truth for task definitions.

**If session ends unexpectedly:**
1. Re-run `/dev-workflow:execute-plan [plan-file]`
2. TodoWrite shows which tasks are complete
3. Skip completed tasks, continue from first pending

Commands:
- /dev-workflow:resume - Continue execution from TodoWrite state
- /dev-workflow:abandon - Clear TodoWrite and stop

### Post-Execution Actions

After all tasks complete, the orchestrator must:

1. **Code Review** - Dispatch code-reviewer agent:
   ```claude
   Task:
     subagent_type: dev-workflow:code-reviewer
     model: opus
     run_in_background: true
     description: "Review all changes"
     prompt: "Review changes from plan execution. git diff main..HEAD"
   ```

   Wait for results:
   ```claude
   TaskOutput:
     task_id: <code-reviewer-task-id>
     block: true
   ```

2. **Process Feedback** - Use `Skill("dev-workflow:receiving-code-review")`

3. **Finish Branch** - Use `Skill("dev-workflow:finishing-a-development-branch")`

These steps are MANDATORY after swarm execution.

---

## Executing Existing Plans

When user has an existing plan file (from brainstorm, previous session, or external source):

### Step 1: Read and Validate

```
Read the plan file
Verify it has Task format: "### Task N: [Name]"
Check for TDD instructions in each task
```

### Step 2: Ask User Approach

Use AskUserQuestion to confirm execution:

```
AskUserQuestion:
  header: "Execution"
  question: "How should I execute this plan?"
  multiSelect: false
  options:
    - label: "Sequential (Recommended)"
      description: "Execute tasks one by one with full TDD cycle"
    - label: "Parallel via swarm"
      description: "Enter plan mode, adapt plan, launch swarm"
    - label: "Review first"
      description: "Let me review and suggest improvements"
```

### Step 3a: Sequential Execution

For each task in order:
1. Create TodoWrite with all tasks
2. Mark current task `in_progress`
3. Follow TDD instructions embedded in task
4. Commit after task passes
5. Mark task `completed`, move to next

After all tasks:
- Dispatch code-reviewer
- Use receiving-code-review skill
- Use finishing-a-development-branch skill

### Step 3b: Parallel via Swarm

1. Use `EnterPlanMode`
2. Adapt existing plan to native format if needed
3. Write to plan file
4. `ExitPlanMode(launchSwarm: true)`
5. Follow Post-Swarm Actions

### Step 3c: Review First

1. Analyze plan against codebase
2. Identify issues or improvements
3. Present findings to user
4. Ask if user wants to proceed or modify
