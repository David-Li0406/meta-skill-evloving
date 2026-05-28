# Orchestration Tools Reference

```
┌─────────────────────────────────────────────────────────────┐
│  Your toolkit for turning ambitious requests into reality.  │
│  Master these tools, and complex work becomes effortless.   │
└─────────────────────────────────────────────────────────────┘
```

## Table of Contents

1. [AskUserQuestion (Most Important)](#askuserquestion)
2. [Agent Types](#agent-types)
3. [Task Tool](#task-tool)
4. [Subagent Prompting Guide](#subagent-prompting-guide)
5. [TaskOutput Tool](#taskoutput-tool)
6. [Task Management](#task-management)
7. [Agent-Task Workflow](#agent-task-workflow)

---

## AskUserQuestion

**Your most important tool.** When you need user input, ALWAYS use this tool. Never present text-only menus.

### Why This Tool Matters

```
┌──────────────────────────────────────────────────┐
│  Text menu:          vs    AskUserQuestion:      │
│                                                  │
│  "Pick one:                 [Visual buttons]     │
│   1. Option A               [Rich descriptions]  │
│   2. Option B               [One click to pick]  │
│   3. Option C"              [Multiple questions] │
│                                                  │
│  Slow, error-prone          Fast, delightful     │
└──────────────────────────────────────────────────┘
```

### The Maximal Philosophy

```
┌──────────────────────────────────────────────────┐
│                                                  │
│   GO MAXIMAL                                     │
│                                                  │
│   • 4 questions when gathering context           │
│   • 4 options per question                       │
│   • RICH descriptions (no length limit!)         │
│   • Creative options they haven't considered     │
│   • Cover every relevant dimension               │
│   • Be a consultant, not a waiter                │
│                                                  │
│   Descriptions can be full sentences,            │
│   explain trade-offs, give examples,             │
│   mention implications. GO DEEP.                 │
│                                                  │
│   Users don't know what they want until          │
│   they see the options. Surface dimensions       │
│   they haven't thought about.                    │
│                                                  │
└──────────────────────────────────────────────────┘
```

### Golden Rules

| Rule                           | Why                                                     |
| ------------------------------ | ------------------------------------------------------- |
| **4 questions when unclear**   | Explore every dimension of the request                  |
| **4 options per question**     | Comprehensive choices, including creative angles        |
| **Recommended first**          | Guide users toward the best choice with "(Recommended)" |
| **Rich descriptions**          | Help users make informed decisions quickly              |
| **multiSelect where relevant** | Let them pick multiple when choices aren't exclusive    |
| **Never text menus**           | Always use the tool. No exceptions.                     |

### Comprehensive Example

```python
AskUserQuestion(questions=[
    {
        "question": "What's the scope you're envisioning?",
        "header": "Scope",
        "options": [
            {"label": "Production-ready (Recommended)", "description": "Full implementation with tests, error handling, docs"},
            {"label": "Functional MVP", "description": "Core feature working, polish later"},
            {"label": "Prototype/spike", "description": "Explore feasibility, throwaway code OK"},
            {"label": "Just the design", "description": "Architecture and plan only, no code yet"}
        ],
        "multiSelect": False
    },
    {
        "question": "What matters most for this feature?",
        "header": "Priority",
        "options": [
            {"label": "User experience", "description": "Smooth, intuitive, delightful to use"},
            {"label": "Performance", "description": "Fast, efficient, scales well"},
            {"label": "Maintainability", "description": "Clean code, easy to extend later"},
            {"label": "Ship speed", "description": "Get it working ASAP, refine later"}
        ],
        "multiSelect": True
    },
    {
        "question": "Any technical constraints I should know?",
        "header": "Constraints",
        "options": [
            {"label": "Must match existing patterns", "description": "Follow conventions already in codebase"},
            {"label": "Specific tech/library required", "description": "You have preferences on tools to use"},
            {"label": "Backward compatibility", "description": "Can't break existing functionality"},
            {"label": "No constraints", "description": "Free to choose the best approach"}
        ],
        "multiSelect": True
    },
    {
        "question": "How should I handle edge cases?",
        "header": "Edge Cases",
        "options": [
            {"label": "Comprehensive (Recommended)", "description": "Handle all edge cases, defensive coding"},
            {"label": "Happy path focus", "description": "Main flow solid, edge cases basic"},
            {"label": "Fail fast", "description": "Throw errors early, let caller handle"},
            {"label": "Graceful degradation", "description": "Always return something usable"}
        ],
        "multiSelect": False
    }
])
```

### Domain-Specific Question Banks

**For implementation tasks:**

- Scope (production/MVP/prototype/design-only)
- Priority (UX/performance/maintainability/speed)
- Constraints (patterns/tech/compatibility/none)
- Edge case handling

**For bug fixes:**

- Urgency (critical/important/when-possible)
- Fix approach (minimal/comprehensive/refactor)
- Testing expectations
- Related areas to check

**For reviews:**

- Focus areas (security/performance/quality/all)
- Depth (quick/standard/comprehensive)
- Output format (comments/report/both)
- Action expectations (approve/block/advise)

---

## Agent Types

```
┌─────────────────────────────────────────────────────────────┐
│  Choose the right agent for the job:                        │
│                                                             │
│  🔍 Explore      → Finding things, understanding codebase   │
│  📋 Plan         → Designing approaches, architecture       │
│  🔧 general-purpose → Building, implementing, executing     │
│  📚 claude-code-guide → Questions about Claude Code         │
└─────────────────────────────────────────────────────────────┘
```

| Agent Type          | Best For                                      | Strengths                       |
| ------------------- | --------------------------------------------- | ------------------------------- |
| `Explore`           | Finding files, patterns, understanding code   | Fast, focused, low-cost         |
| `Plan`              | Architecture decisions, implementation design | Systematic analysis, trade-offs |
| `general-purpose`   | Implementation, complex multi-step work       | Full tool access, autonomous    |
| `claude-code-guide` | Claude Code feature questions                 | Documentation expertise         |

### Quick Selection Guide

| User Says                           | Agent Type          |
| ----------------------------------- | ------------------- |
| "Find X" / "Where is Y"             | `Explore`           |
| "How should we implement X"         | `Plan`              |
| "Build X" / "Fix Y" / "Implement Z" | `general-purpose`   |
| "Can Claude Code do X"              | `claude-code-guide` |

---

## Task Tool

Spawn an agent to handle work. This is how you delegate.

**Remember:** Subagents do NOT inherit skills. They only know what you tell them in the prompt. You are the conductor — they are the musicians.

### Parameters

| Parameter           | Required | Description                                    |
| ------------------- | -------- | ---------------------------------------------- |
| `subagent_type`     | Yes      | Agent type to spawn                            |
| `prompt`            | Yes      | Detailed instructions for the agent            |
| `description`       | Yes      | Short 3-5 word summary                         |
| `run_in_background` | **Yes**  | **ALWAYS set to True** for async orchestration |
| `model`             | No       | Override model (haiku, sonnet, opus)           |

### Background Agents: The Default

**ALWAYS use `run_in_background=True`.** This is the foundation of powerful orchestration.

```python
# Correct: Background agents (ALWAYS)
Task(subagent_type="Explore", prompt="...", run_in_background=True)
Task(subagent_type="general-purpose", prompt="...", run_in_background=True)
```

### The Notification System

When background agents complete, you receive automatic notifications:

```xml
<agent-notification>
  <agent-id>abc123</agent-id>
  <output-file>/tmp/claude/.../tasks/abc123.output</output-file>
  <status>completed</status>
  <summary>Agent "PR Review" completed.</summary>
</agent-notification>
```

**This enables true async orchestration:**

- Launch multiple agents
- Continue working OR update the user
- Notifications arrive as agents complete
- Process results, launch more agents as needed

### Your Freedom After Launching

| Situation                    | What To Do                                        |
| ---------------------------- | ------------------------------------------------- |
| More independent work exists | Continue working, notifications arrive when ready |
| Nothing else right now       | Update user on status, yield turn                 |
| User should see progress     | Show active work in signature                     |
| Waiting on specific result   | Work on other things until that notification      |

### Reading Agent Results

When notification arrives, read the output file:

```python
Read(file_path="/tmp/claude/.../tasks/abc123.output")
```

Or use TaskOutput:

```python
TaskOutput(task_id="abc123")
```

### Model Selection

| Task Complexity        | Model           | Why                          |
| ---------------------- | --------------- | ---------------------------- |
| Simple search/patterns | `haiku`         | Fast and cheap               |
| Standard exploration   | `haiku`         | Sufficient for most searches |
| Complex exploration    | `sonnet`        | Needs reasoning              |
| Simple implementation  | `haiku`         | Pattern-based work           |
| Complex implementation | `sonnet`        | Design decisions needed      |
| Architecture/planning  | `sonnet`/`opus` | Complex trade-offs           |
| Security review        | `sonnet`        | Careful analysis             |

### Parallelism Strategy

| Priority     | Approach                                         |
| ------------ | ------------------------------------------------ |
| **Speed**    | Parallelize with sonnet, accept higher cost      |
| **Cost**     | Sequential haiku where possible                  |
| **Balanced** | Haiku for exploration, sonnet for implementation |

---

## Subagent Prompting Guide

Your agents are only as good as your prompts. Invest in clear instructions.

### The WORKER Preamble (Required)

**Every agent prompt MUST start with this preamble:**

```
CONTEXT: You are a WORKER agent, not an orchestrator.

RULES:
- Complete ONLY the task described below
- Use tools directly (Read, Write, Edit, Bash, etc.)
- Do NOT spawn sub-agents
- Do NOT call TaskCreate or TaskUpdate
- Report your results with absolute file paths

CODE STANDARDS (MANDATORY):
- NO mock implementations or stubs
- NO placeholder code or TODOs
- NO simulated or fake data
- ALL code must be production-ready and deployable
- Use REAL integrations (actual SDKs, APIs, databases)
- Include proper error handling and input validation
- Use environment variables for configuration
- If implementation details are unknown, ASK — never guess

AVOID AI SLOP:
- NO excessive comments — only add comments a human would add, match existing file style
- NO unnecessary defensive checks — don't add try/catch or null checks for trusted/validated codepaths
- NO TypeScript `any` casts to bypass type issues — fix the types properly
- MATCH the existing code style — be consistent with the file and codebase conventions
- WRITE like a human — concise, practical, no over-engineering

TASK:
[Your specific task here]
```

This prevents agents from recursively trying to orchestrate and ensures all code is production-ready.

### The Five Elements

After the preamble, include:

```
┌─────────────────────────────────────────────────────────────┐
│  1. PREAMBLE   → WORKER context and rules (required!)       │
│  2. CONTEXT    → What's the bigger picture?                 │
│  3. SCOPE      → What exactly should this agent do?         │
│  4. CONSTRAINTS → What rules or patterns to follow?         │
│  5. OUTPUT     → What should the agent return?              │
└─────────────────────────────────────────────────────────────┘
```

### Example: Implementation Prompt

```
CONTEXT: You are a WORKER agent, not an orchestrator.

RULES:
- Complete ONLY the task described below
- Use tools directly (Read, Write, Edit, Bash, etc.)
- Do NOT spawn sub-agents
- Do NOT call TaskCreate or TaskUpdate
- Report your results with absolute file paths

CODE STANDARDS (MANDATORY):
- NO mock implementations or stubs
- NO placeholder code or TODOs
- NO simulated or fake data
- ALL code must be production-ready and deployable
- Use REAL integrations (actual SDKs, APIs, databases)
- Include proper error handling and input validation
- Use environment variables for configuration
- If implementation details are unknown, ASK — never guess

AVOID AI SLOP:
- NO excessive comments — only add comments a human would add, match existing file style
- NO unnecessary defensive checks — don't add try/catch or null checks for trusted/validated codepaths
- NO TypeScript `any` casts to bypass type issues — fix the types properly
- MATCH the existing code style — be consistent with the file and codebase conventions
- WRITE like a human — concise, practical, no over-engineering

TASK:
Create server/src/routes/auth.js with:
- POST /signup - Create user, hash password with bcrypt, return JWT
- POST /login - Verify credentials, return JWT

CONTEXT: Building a Todo app with Express backend and SQLite.
The users table exists in server/src/db/database.js.

CONSTRAINTS:
- Use the existing db from database.js
- JWT secret from process.env.JWT_SECRET
- Follow existing code patterns

RETURN: Confirm files created and summarize implementation.
```

### Example: Exploration Prompt

```
CONTEXT: You are a WORKER agent, not an orchestrator.

RULES:
- Complete ONLY the task described below
- Use tools directly (Read, Write, Edit, Bash, etc.)
- Do NOT spawn sub-agents
- Do NOT call TaskCreate or TaskUpdate
- Report your results with absolute file paths

CODE STANDARDS (MANDATORY):
- NO mock implementations or stubs
- NO placeholder code or TODOs
- NO simulated or fake data
- ALL code must be production-ready and deployable
- Use REAL integrations (actual SDKs, APIs, databases)
- Include proper error handling and input validation
- Use environment variables for configuration
- If implementation details are unknown, ASK — never guess

AVOID AI SLOP:
- NO excessive comments — only add comments a human would add, match existing file style
- NO unnecessary defensive checks — don't add try/catch or null checks for trusted/validated codepaths
- NO TypeScript `any` casts to bypass type issues — fix the types properly
- MATCH the existing code style — be consistent with the file and codebase conventions
- WRITE like a human — concise, practical, no over-engineering

TASK:
Find all files related to user authentication.

Look for:
- Route handlers for login/signup/logout
- Middleware that checks authentication
- Session or token management
- User model or schema

RETURN: List of files with brief description of each.
```

### Prompt Anti-Patterns

| Bad                  | Problem           | Good                                                |
| -------------------- | ----------------- | --------------------------------------------------- |
| "Fix the bug"        | Which bug? Where? | "Fix the 401 error after password reset in auth.js" |
| "Build the frontend" | Too broad         | Split into: components, routing, state, API         |
| "Implement auth"     | No constraints    | Specify: framework, token type, file locations      |
| "Check the code"     | No focus          | "Review for SQL injection, return severity ratings" |

### Scoping Work

| Scope                    | Approach             |
| ------------------------ | -------------------- |
| 1 file                   | One agent            |
| 2-3 related files        | One agent            |
| Multiple unrelated files | Parallel agents      |
| Full feature (5+ files)  | Decompose into tasks |

---

## TaskOutput Tool

Retrieve results from background agents.

```python
# Wait for completion
result = TaskOutput(task_id="abc123")

# Check without waiting
result = TaskOutput(task_id="abc123", block=False)

# Wait with timeout
result = TaskOutput(task_id="abc123", timeout=60000)
```

---

## Task Management

**Always use TaskCreate for multi-step work.** This is how you track and coordinate.

### TaskCreate

```python
TaskCreate(
    subject="Implement user authentication",
    description="JWT-based auth with login/logout endpoints, password hashing..."
)
```

### TaskUpdate

```python
# Set dependency
TaskUpdate(taskId="2", addBlockedBy=["1"])

# Add progress note
TaskUpdate(taskId="1", addComment={
    "author": "orchestrator",
    "content": "Schema design complete"
})

# Mark done
TaskUpdate(taskId="1", status="resolved")
```

### TaskList & TaskGet

```python
TaskList()          # See all tasks with status
TaskGet(taskId="1") # Get full details of one task
```

---

## Agent-Task Workflow

The complete flow for orchestrated execution:

```
┌─────────────────────────────────────────────────────────────┐
│  1. DECOMPOSE                                               │
│     TaskCreate → TaskCreate → TaskCreate                    │
│                                                             │
│  2. SET DEPENDENCIES                                        │
│     TaskUpdate(addBlockedBy=[...])                          │
│                                                             │
│  3. FIND READY WORK                                         │
│     TaskList() → find tasks with empty blockedBy            │
│                                                             │
│  4. SPAWN BACKGROUND AGENTS                                 │
│     Task(..., run_in_background=True) ← ALWAYS background   │
│                                                             │
│  5. CONTINUE OR YIELD                                       │
│     More work? Continue. Otherwise update user, yield.      │
│                                                             │
│  6. PROCESS NOTIFICATIONS                                   │
│     <agent-notification> arrives → Read results             │
│     Mark TaskUpdate(status="resolved")                      │
│                                                             │
│  7. REPEAT                                                  │
│     Back to step 3 until all done                           │
└─────────────────────────────────────────────────────────────┘
```

### Example Flow

```python
# 1. Decompose
TaskCreate(subject="Setup database schema", description="...")
TaskCreate(subject="Implement auth routes", description="...")
TaskCreate(subject="Build auth middleware", description="...")

# 2. Dependencies
TaskUpdate(taskId="2", addBlockedBy=["1"])
TaskUpdate(taskId="3", addBlockedBy=["2"])

# 3. Find ready (task 1 is unblocked)
TaskList()

# 4. Spawn background agent (ALWAYS background)
Task(subagent_type="general-purpose",
     description="Setup database",
     prompt="Create SQLite database with users table...",
     run_in_background=True)

# 5. Update user and yield (or continue other work)
"Setting up the database schema..."
# ─── ◈ Orchestrating ── Database Setup ──

# 6. Notification arrives
# <agent-notification>
#   <agent-id>xyz789</agent-id>
#   <status>completed</status>
# </agent-notification>

# Read results, mark complete
Read(file_path="...output file...")
TaskUpdate(taskId="1", status="resolved")

# 7. Repeat - task 2 now unblocked
TaskList()
# Launch next agent...
```

---

## Best Practices Summary

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ✓ ALWAYS use run_in_background=True for agents             │
│  ✓ Always use AskUserQuestion for user input                │
│  ✓ Decompose before spawning agents                         │
│  ✓ Set dependencies explicitly                              │
│  ✓ Launch multiple background agents in single message      │
│  ✓ Rich, detailed prompts for agents                        │
│  ✓ Process notifications as they arrive                     │
│  ✓ Mark tasks resolved immediately when done                │
│  ✓ Show active work in signature                            │
│                                                             │
│  ✗ Never use foreground (blocking) agents                   │
│  ✗ Never use text menus for choices                         │
│  ✗ Never run independent work sequentially                  │
│  ✗ Never give vague prompts to agents                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

```
─── ◈ Tools Reference Complete ──────────────────
```
