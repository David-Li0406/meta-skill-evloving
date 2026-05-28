---
name: spawn
description: How to spawn subagents correctly. Use this reference when you need to delegate work to a specialized agent.
---

# Spawning Subagents

## Why Subagents

1. **Model efficiency**: Orchestrator uses opus, subagents use cheaper models
2. **Context isolation**: Subagent work doesn't flood main context
3. **Parallelization**: Multiple subagents can work simultaneously
4. **Focus**: Each agent has a specific role with clear constraints

## How to Spawn

Use the Task tool with these parameters:

```json
{
  "description": "3-5 word summary",
  "prompt": "Detailed instructions for the agent",
  "subagent_type": "Explore|Plan|general-purpose",
  "model": "haiku|sonnet|opus"
}
```

## Agent Selection

| Need | Agent | Default Model | subagent_type |
|------|-------|---------------|---------------|
| Find code/files | explorer | haiku | Explore |
| Web/doc research | researcher | haiku | general-purpose |
| Plan implementation | architect | sonnet | Plan |
| Write code | implementer | sonnet | general-purpose |
| Review changes | reviewer | sonnet | general-purpose |
| Fix bugs | debugger | sonnet | general-purpose |
| Git operations | git-agent | haiku | general-purpose |

## Self-Model-Selection

Agents can downgrade their model when task is simpler than expected:

```
[In subagent prompt, agent can say:]
"This is straightforward - spawning with haiku instead of sonnet"
```

**Model selection criteria:**

| Complexity | Indicators | Model |
|------------|------------|-------|
| trivial | Single pattern search, one file change, simple command | haiku |
| simple | Clear logic, existing pattern to follow, <50 lines | haiku or sonnet |
| medium | Some reasoning needed, multiple considerations | sonnet |
| complex | Architectural decisions, novel patterns, tricky edge cases | sonnet |
| very complex | Cross-cutting concerns, security implications | opus (rare, ask orchestrator) |

**Rules:**
- Can always downgrade (sonnet → haiku)
- Never upgrade without asking orchestrator
- Default to cheaper when unsure
- If haiku struggles, retry with sonnet (not automatic, must be explicit)

**Example:**
```
Orchestrator spawns implementer (default: sonnet) to add a button.
Implementer sees: "Just adding one onClick handler to existing component."
Implementer says: "Trivial task, using haiku" and spawns sub-agent with haiku.
```

## Prompt Structure

Every subagent prompt MUST include:

1. **Task**: What exactly to do (one clear objective)
2. **Scope**: What files/areas to touch
3. **Output**: What to return (be specific about format)
4. **Constraints**: What NOT to do

### Example Prompts

**Explorer (finding code):**
```
Find all authentication-related code.

Scope: src/ directory
Output: List of file:line references with one-line descriptions
Constraints: Don't read file contents, just locate. Use Serena tools.
```

**Implementer (writing code):**
```
Add input validation to the login form.

Scope: src/components/LoginForm.tsx only
Output: Summary of changes made
Constraints: Don't modify other files. Don't add new dependencies.
Follow existing patterns in the codebase.
```

**Reviewer (checking code):**
```
Review changes to authentication flow.

Scope: Files modified in current branch vs main
Output: PASS or NEEDS_CHANGES with specific issues
Constraints: Focus on bugs and security. Skip style issues.
```

## Parallel Spawning

When tasks are independent, spawn multiple in one message:

```
I'll spawn three subagents in parallel:
1. Explorer to find auth files
2. Explorer to find test files
3. Researcher to get latest JWT best practices

[Three Task tool calls in same message]
```

## Recursive Spawning

Subagents CAN spawn more subagents when:
- Task is too large for one agent
- Multiple independent subtasks discovered
- Parallelization would help

**Example: Explorer finds large codebase**
```
Explorer finds 50 auth-related files. Instead of returning all:
1. Spawn 5 sub-explorers, each handling 10 files
2. Each sub-explorer returns summarized findings
3. Main explorer aggregates into final report
```

**Model inheritance:**
- Subagent uses same or cheaper model
- Never spawn opus from haiku
- haiku → haiku (OK)
- sonnet → haiku (OK, for simple subtasks)
- sonnet → sonnet (OK, for complex subtasks)

**Depth limit:** Max 3 levels deep to prevent runaway spawning
- Orchestrator (opus) → Agent (sonnet/haiku) → Sub-agent → Sub-sub-agent

## Anti-Patterns

**DON'T:**
- Spawn subagent for one-liner tasks
- Use opus model for subagents (reserved for orchestrator)
- Give vague prompts like "look around"
- Spawn subagent to do what you could do in 2 tool calls
- Spawn more than 5 parallel subagents (coordination overhead)

**DO:**
- Batch related work into one subagent
- Specify exact output format
- Use cheapest model that can do the job
- Set clear scope boundaries
- Let agents spawn sub-agents for large tasks

## Subagent Context

Subagents receive:
- The prompt you provide
- Agent rules from AGENT_RULES.md (via hook injection)
- Access to same tools as you

Subagents do NOT receive:
- Your conversation history
- Current phase/state (unless you tell them)
- Other subagents' results (unless you include them)

## Permission Awareness

When spawning subagents within a workflow:

1. **Include phase context**: Tell subagents what phase they're in and what tools are blocked
2. **Pass workflow ID**: Include workflow ID so subagents can query permissions
3. **Self-enforcement**: Subagents should check permissions before file operations

**Example prompt with permission context:**
```
Implement input validation for login form.

**Workflow Context:**
- Workflow: iterate (implement phase)
- Blocked tools: None in this phase
- File restrictions: Only modify src/components/LoginForm.tsx

**Permission check:** Use `is_tool_allowed("Edit", file_path=path)` if unsure.
```

**Programmatic check** (lib/permission_query.py):
```python
from permission_query import get_permissions, is_tool_allowed

# Subagent checks before editing
allowed, reason = is_tool_allowed("Edit", file_path="src/main.py")
if not allowed:
    print(f"Cannot edit: {reason}")
```

**Orchestrator phase**: In ORCHESTRATE phase, Edit/Write/Bash are blocked - you MUST spawn subagents for all implementation work.
