---
name: iterate
description: Autonomous TDD implementation workflow with phase gates
user_invocable: true
---

# Iterate Workflow

TDD development loop with phase gates. Works autonomously until exit conditions met.

## Initialize (REQUIRED FIRST STEP)

**Run this command immediately to start the workflow:**

```bash
python3 ~/.claude/plugins/agent-swarm/lib/iterate_workflow.py $ARGUMENTS
```

The workflow auto-initializes when invoked. This creates the state file that subagents need for TDD context.

## Flow

**With ORCHESTRATE (main agent coordinates workers):**
```
ORCHESTRATE ──┬──→ [spawn subagents] ──→ queue empty? ──→ done
              │                              ↓
              └──────────── no ←─────────────┘
```

**Subagents (TDD loop):**
```
test_writing → implement → test → review → done
      ↑            ↑         |       |
      |            |         v       v
      +-- coverage +-- fail -+  issues
```

## Phases

| Phase | Purpose | Allowed Tools |
|-------|---------|---------------|
| **orchestrate** | Main agent coordinates workers | Read, Task, TaskOutput, TodoWrite (NO Edit/Write/Bash!) |
| **test_writing** | Write tests first (spec) | Read, Glob, Grep, Edit, Write, Bash |
| **implement** | Make tests pass | Read, Glob, Grep, Edit, Write, Bash |
| **test** | Run pytest, lint, coverage | Read, Glob, Grep, Bash (no editing!) |
| **review** | Fix Greptile issues | Read, Glob, Grep, Edit, Write, Bash |

## Orchestrator Role

**When in ORCHESTRATE phase, you NEVER do implementation tasks. Edit/Write/Bash are BLOCKED.**

The ORCHESTRATE phase enforces the orchestrator role through tool restrictions:
- ✅ Read, Task, TaskOutput, TodoWrite - coordination tools
- ❌ Edit, Write, NotebookEdit, Bash - blocked, spawn agents instead

### Rules
- 1 task → spawn 1 agent
- 5 tasks → spawn 5 agents in parallel
- No exceptions - you cannot edit code yourself

### Orchestrator responsibilities (ORCHESTRATE phase)
- Read specs/queue files
- Spawn subagents via Task tool
- Monitor completions via TaskOutput
- Track progress via TodoWrite
- Check completion: `is_orchestration_complete()` → queue empty AND no workers

### What the orchestrator does NOT do
- **Does NOT evaluate agent work quality** - agents are responsible for their own verification
- **Does NOT run tests** - test/review agents handle that
- **Does NOT review code** - reviewer agents handle that
- Just spawns agents, takes output, updates queue

Future: Autokill feature may terminate long-running or failing agents.

### Insufficient context → Go back to INTAKE
If the orchestrator cannot write quality prompts because it lacks context:

**Orchestrator does NOT explore in ORCHESTRATE.** Go back to INTAKE phase.

INTAKE is where orchestrator context gathering happens:
- Explore codebase
- Read relevant files
- Understand scope and patterns
- Gather requirements

**If you're in ORCHESTRATE and can't write good prompts:**
```bash
python3 lib/iterate_workflow.py set-phase intake
```

Then complete intake properly before returning to orchestrate.

**Signs you rushed intake:**
- Writing vague prompts like "implement spec.md"
- Not knowing which files to reference
- Unclear on existing patterns
- Missing acceptance criteria

### Subagents explore current code
Subagents are close to the code - they explore their specific area of the **current codebase**:
- Read related files to understand patterns
- Grep for similar implementations
- Check for side effects before changes
- Find existing code to follow

**NOT web searches.** Subagents understand the code they're changing, not researching external topics.
Web/external research happens in RESEARCH phase (orchestrator responsibility).

### Subagent responsibilities (TDD loop phases)
- Write tests (test_writing phase)
- Write/modify code (implement phase)
- Fix review issues (review phase)

## Explore-Before-Prompt Pattern

**When orchestrator has insufficient context for good prompts, use this pattern WITHIN a task.**

Unlike going back to INTAKE (full phase change), this pattern lets the orchestrator spawn an explorer for ONE task, get context, then spawn implementer with enriched prompt.

### When to use exploration

The orchestrator should spawn an explorer agent BEFORE spawning an implementer when:
- Task references files/modules not yet read by orchestrator
- Task description is vague (< 10 words, no file paths)
- Task uses vague verbs ("improve", "fix") without specifics
- Task mentions "similar to X" without providing examples
- No code snippets or file paths in available context

**Detection helper:**
```python
from exploration_helpers import needs_exploration

if needs_exploration(task, context):
    # Spawn explorer first, then implementer
```

### Exploration workflow

```
1. Detect: needs_exploration(task, context) → True
2. Explore: Spawn explorer with targeted prompt
3. Enrich: Add explorer output to context
4. Implement: Spawn implementer with enriched prompt
```

**Example:**

```python
# Bad: vague prompt
Task(
    description="Fix auth system",
    subagent_type="agent-swarm:implementer",
    prompt="Fix the authentication system bugs"
)

# Good: explore-first
from exploration_helpers import needs_exploration, detect_exploration_type, format_explorer_prompt

task = {"description": "Fix auth system"}
context = {"files_read": [], "code_snippets": []}

if needs_exploration(task, context):
    # Spawn explorer
    exploration_type = detect_exploration_type(task)
    explorer_prompt = format_explorer_prompt(exploration_type, task)

    explorer_result = Task(
        description="Explore auth system",
        subagent_type="agent-swarm:explorer",
        model="haiku",
        token_budget=50000,
        prompt=explorer_prompt
    )

    # Wait for explorer result, then spawn implementer
    enriched_context = {**context, "exploration": explorer_result}

    Task(
        description="Fix auth token expiration",
        subagent_type="agent-swarm:implementer",
        model="opus",
        token_budget=100000,
        prompt=f"""Fix auth token expiration bug.

**Context from Exploration:**
{explorer_result}

**Requirements:**
- Token should expire after 24h
- Refresh tokens should work
- Tests must pass

Follow patterns shown in exploration output."""
    )
```

### Exploration types

| Type | When to Use | What Explorer Returns |
|------|-------------|----------------------|
| `file_discovery` | Task mentions files/modules | File paths, key functions, entry points |
| `pattern_matching` | Task says "similar to X" | Existing implementations, patterns, helpers |
| `dependency_mapping` | Task modifies existing code | Callers, imports, side effects, tests |
| `context_enrichment` | Task is vague | Directory structure, key files, patterns |

**Prompt templates available in `lib/prompt_templates.py`:**
```python
from prompt_templates import EXPLORATION_PROMPTS, IMPLEMENTER_PROMPTS

# Get exploration prompt template
explorer_prompt = EXPLORATION_PROMPTS["file_discovery"].format(topic="authentication")

# Get implementer prompt template
implementer_prompt = IMPLEMENTER_PROMPTS["with_exploration"].format(
    task_description="Fix auth bug",
    explorer_output="...",
    requirements="...",
    suggested_files="..."
)
```

### When NOT to use this pattern

- **Orchestrator phase change needed**: If ALL tasks need context, go back to INTAKE phase
- **Subagent exploration sufficient**: Let implementers explore their specific area during work
- **Context already available**: If you have files, patterns, examples already

**Rule of thumb:**
- Missing context for 1-2 tasks? → Explore-before-prompt pattern
- Missing context for ALL tasks? → Go back to INTAKE phase



## Task Queue (Fundamental)

**ALL work flows through the task queue.** This is not optional infrastructure - it's the enforcement mechanism that ensures subagents are spawned.

### Queue Flow

```
IMPLEMENT phase:
  Identify work → Add to queue → Spawn agents → Mark done → Push when queue empty

REVIEW phase:
  Get comments → Add to queue → Spawn agents → Mark done → Push when queue empty
```

### Queue Operations

| Operation | When | API |
|-----------|------|-----|
| Add task | After decomposing work | `workflow_queue.add_task(task)` |
| Spawn agents | After populating queue | `Task(...)` for each item (up to max parallel) |
| Mark done | After agent completes | `workflow_queue.mark_done(task_id)` |
| Check empty | Before push | `workflow_queue.all_complete(pr_id)` |

### Push Triggers

Push happens when:
- Implementation batch is complete (queue empty after implement phase)
- Review comments are all addressed (queue empty after review fixes)

**Do NOT push after each task.** Wait for the batch.

### Dynamic Queue Updates

The queue can grow during execution:
- New implementation tasks discovered during work
- New review comments after push
- Dependencies identified by subagents

The orchestrator monitors and repopulates as needed.

## Parallel Execution

Spawn up to `config.orchestrate.max_agents` agents in ONE message block to run simultaneously:

```
Task(description="Implement module A", subagent_type="agent-swarm:implementer", prompt="...")
Task(description="Implement module B", subagent_type="agent-swarm:implementer", prompt="...")
Task(description="Implement module C", subagent_type="agent-swarm:implementer", prompt="...")
```

Even for a single task:
```
Task(description="Implement module A", subagent_type="agent-swarm:implementer", prompt="...")
```

**Non-blocking monitoring:** Use `TaskOutput` with `block=false` to check agent status without waiting. The orchestrator continues working while agents run in background.

```python
# Good: non-blocking check
result = TaskOutput(task_id=agent_id, block=False, timeout=1000)
if result.status == "completed":
    # Process result

# Bad: blocking wait
result = TaskOutput(task_id=agent_id, block=True, timeout=120000)  # DON'T DO THIS
```

## Subagent Prompting

When spawning implementer agents, your prompt must include:

1. **Architectural context** - How the component fits in the system design
2. **Constraints** - What NOT to do and why (prevent logical-but-wrong fixes)
3. **Design intent** - The "why" behind existing code/restrictions
4. **TDD instruction** - Agents must write tests FIRST, then implement

**IMPORTANT:** Every implementer prompt MUST include:
```
**TDD:** Write tests FIRST that specify the expected behavior, then implement code to make tests pass, then verify all tests pass.
```

One agent handles the complete TDD cycle. Do NOT spawn separate agents for test-writing and implementation.

**Example prompt structure:**
```
**Context:** [How this component relates to the system architecture]

**Constraint:** Do NOT [specific thing to avoid] because [reason].

**Task:** [Specific work to do]

**TDD:** Write tests FIRST that specify the expected behavior, then implement code to make tests pass, then verify all tests pass.

**Verification:** [How to verify the fix is correct]
```

Without architectural context, agents may make fixes that pass tests but break system invariants.

## Kick-back Logic

After `test` phase, results determine next phase:

| Result | Next Phase | Why |
|--------|------------|-----|
| All pass | review | Ready for code review |
| Coverage low | test_writing | Need more tests |
| Tests fail | implement | Fix code |
| Lint fail | implement | Fix code |

After `review` phase:

| Result | Next Phase | Why |
|--------|------------|-----|
| Clean | done | Workflow complete |
| Issues | implement | Fix review comments |

## Usage

```bash
# Start iterate workflow
/iterate "Add user validation feature"

# With custom max iterations
/iterate --max 10 "Refactor auth module"
```

## CLI Commands

```bash
# Start workflow
python3 lib/iterate_workflow.py start "task description" [max_iterations]

# Check status
python3 lib/iterate_workflow.py status

# Get current phase
python3 lib/iterate_workflow.py phase

# Advance to next phase
python3 lib/iterate_workflow.py advance

# Record test results (after running pytest, lint, coverage)
python3 lib/iterate_workflow.py test <tests> <lint> <coverage>
# Use 1=pass, 0=fail. Example: test 1 1 0 (tests pass, lint pass, coverage fail)

# Record review status
python3 lib/iterate_workflow.py review <clean>
# Use 1=clean, 0=issues

# Stop workflow
python3 lib/iterate_workflow.py stop
```

## Test Phase Verification

In the `test` phase, run these checks:

```bash
# 1. Run tests
pytest tests/ -v

# 2. Run lint
ruff check .

# 3. Run coverage
pytest --cov=. --cov-report=term-missing

# 4. Record results
python3 lib/iterate_workflow.py test 1 1 1  # if all pass
python3 lib/iterate_workflow.py test 1 0 1  # if lint failed
python3 lib/iterate_workflow.py test 0 1 1  # if tests failed

# 5. Advance phase (kick-back or proceed based on results)
python3 lib/iterate_workflow.py advance
```

## PR Completion Tracking

Work is grouped by logical PRs. The orchestrator MUST track completion properly:

After each agent completes:
1. Update task status: `workflow_queue.mark_done(task_id)`
2. Check if PR ready: `workflow_queue.all_complete(pr_id)`
3. Only push when ALL tasks for PR are done
4. Triggers ONE Greptile review per PR, not per task

**Do NOT:**
- Push after each individual task completes
- Trigger multiple reviews for the same PR

## Review Phase

1. Verify all PR tasks complete (see PR Completion Tracking)
2. Push changes to trigger Greptile review (ONE push per PR)
3. Check for review comments
4. If issues found: `python3 lib/iterate_workflow.py review 0` then `advance`
5. If clean: `python3 lib/iterate_workflow.py review 1` then `advance`

## Orchestrator Progress Output

The orchestrator MUST provide informative output during workflow execution:

### After spawning agents:
```
[SPAWNED] {count} agent(s) for: {task_summaries}
```

### After agent completion:
```
[COMPLETE] {agent_description}: {brief_result_summary}
```

### Before phase transitions:
```
[PHASE] {current_phase} → {next_phase} | Reason: {reason}
```

### On task queue updates:
```
[QUEUE] {pending_count} pending, {in_progress_count} in progress, {completed_count} completed
```

This output helps users understand workflow progress and aids debugging.

## Exit Conditions

| Condition | Trigger |
|-----------|---------|
| `orchestration_complete` | Queue empty AND no active workers (ORCHESTRATE mode) |
| `review_approved` | Review clean, workflow complete (TDD loop) |
| `max_iterations` | Hit iteration limit (default: 5) |
| `user_stopped` | Manual `/iterate stop` |

## DO NOT

- Skip phases (workflow enforces order)
- Use Edit/Write in test phase (blocked by hook)
- Use Edit/Write/Bash in ORCHESTRATE phase (blocked - spawn agents instead)
- Ignore kick-back (follow the loop)
- Bypass test verification
- Do implementation work yourself (ALWAYS spawn agents)
- Spawn agents sequentially (use ONE message block for parallel execution)
- Split TDD across multiple agents (one agent = complete TDD cycle: test → implement → verify)
- Use blocking TaskOutput calls (orchestrator spawns and monitors, doesn't wait)
- Spawn agents without informative progress output

## Permission Awareness

At task start, check workflow state for active permissions:

1. **Check active workflow**: `get_active_workflow_id()` returns current workflow
2. **Get permissions**: `get_permissions(workflow_id)` returns PermissionStore
3. **Verify tool access**: `is_tool_allowed(tool_name, **context)` before operations

**Self-enforcement**: Do not attempt blocked operations. The phase table above shows allowed tools per phase - respect these restrictions even if hooks don't catch violations.

**Programmatic check** (lib/permission_query.py):
```python
from permission_query import get_permissions, is_tool_allowed

# Check if Edit is allowed
allowed, reason = is_tool_allowed("Edit", file_path="src/main.py")
if not allowed:
    print(f"Blocked: {reason}")
```

**Subagent awareness**: When spawning subagents, include current phase in prompt so they know their tool restrictions.
