---
name: write-task
description: Validates and writes well-formed tasks to .agent/tasks.md. Use when adding tasks, creating tasks, or writing to the task list.
allowed-tools:
  - Bash(node:*)
---

# Write Task Skill

This skill provides the knowledge and tools to write well-formed, self-contained tasks to `.agent/tasks.md`.

## How to Write Tasks

Use the `task_add.js` script to add tasks:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/task_add.js" .agent/tasks.md "Task title
Path: /absolute/path/to/file
Pattern: Reference to existing similar code
Dependencies: What must exist first
Expected: Clear success criteria"
```

## ABSOLUTE PROHIBITIONS

**YOU MUST NEVER:**
- Edit `.agent/tasks.md` directly with Edit or Write tools
- Read `.agent/tasks.md` (you don't need to see it)
- Modify existing tasks
- Do anything except run the task_add.js script

If you are tempted to touch tasks.md directly for ANY reason, STOP. You cannot. You will not. The script is the ONLY way.

## Task Validation Requirements

Before writing ANY task, verify ALL of the following. Reject the task if ANY requirement fails:

### 1. Single Responsibility (MANDATORY)
- Task does exactly ONE thing
- If you can use the word "and" to describe it, it's TOO BIG
- **BAD:** "Create user model and add validation"
- **GOOD:** "Create user model" (separate task for validation)

### 2. Absolute Path Required (MANDATORY)
- `Path:` field must be an absolute path starting with `/`
- **BAD:** `Path: src/utils/helper.ts`
- **GOOD:** `Path: /Users/tom/project/src/utils/helper.ts`

### 3. Pattern Reference (MANDATORY for code tasks)
- `Pattern:` must reference a SPECIFIC existing file
- Cannot be vague or generic
- **BAD:** `Pattern: Follow existing conventions`
- **GOOD:** `Pattern: Follow /Users/tom/project/src/utils/hash.ts`

### 4. Clear Expected Outcome (MANDATORY)
- `Expected:` must describe verifiable completion criteria
- Someone must be able to CHECK if it's done
- **BAD:** `Expected: Working correctly`
- **GOOD:** `Expected: Export signToken(payload) and verifyToken(token) functions`

### 5. Self-Contained Context (MANDATORY)
- Task must include EVERYTHING needed to execute it
- Executor has NO access to conversation history
- Executor has NO access to other tasks
- If context is missing, the task CANNOT be executed

## Rejection Protocol

If a task fails validation, you MUST:

1. **Refuse to write it**
2. **State exactly which requirement(s) failed**
3. **Provide specific guidance on what's missing**

Example rejection:
```
REJECTED: Task fails validation

- Single Responsibility: "Create auth middleware and add rate limiting" does TWO things
- Pattern: "Follow existing patterns" is too vague - need specific file path
+ Path: Valid absolute path provided
+ Expected: Clear success criteria

Provide:
1. Split into two separate tasks
2. Specific file path for Pattern (e.g., /project/src/middleware/logging.ts)
```

## Input Format

Tasks should be formatted as:
```
Task title
Path: /absolute/path
Pattern: /path/to/reference/file
Dependencies: Prerequisites
Expected: Success criteria
Plan: Optional plan reference
```

## Output Format

After successfully writing a task:
```
Added: Task title
```

After rejecting a task:
```
REJECTED: [reason]
[specific guidance]
```

## Remember

Be AGGRESSIVE about quality. A poorly-formed task wastes everyone's time. Better to reject and ask for clarification than to add garbage to the task list.

The task executor is ISOLATED. It sees ONLY the task text. If the task doesn't contain everything needed, execution WILL fail.
