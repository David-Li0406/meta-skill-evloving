---
name: codex-delegation
description: How to delegate implementation tasks to Codex workers via MCP. Use when executing tasks that require code implementation by GPT Codex workers.
---

# Codex Delegation Skill

This skill defines how the CEO (Claude) delegates tasks to Codex workers.

## When to Delegate

Delegate to Codex workers when:
- Task is implementation-focused (writing code)
- Task has clear acceptance criteria
- Task doesn't require strategic decisions
- Task is scoped to specific files

Do NOT delegate when:
- Task requires architecture decisions
- Task is a [VERIFY] checkpoint
- Task requires user interaction
- Task involves research or analysis

## Preparing Context Packages

### Minimal Context Package

```json
{
  "taskId": "1.1",
  "task": {
    "title": "Task title",
    "do": "What to do",
    "doneWhen": "Completion criteria",
    "acceptance": ["Criterion 1", "Criterion 2"]
  }
}
```

### Full Context Package

```json
{
  "taskId": "1.1",
  "task": {
    "title": "Implement user login form",
    "do": "Create login form component at src/components/Login.tsx",
    "doneWhen": "Form renders with email/password fields and validation",
    "acceptance": [
      "Form has email input with validation",
      "Form has password input with masking",
      "Submit button triggers onSubmit handler",
      "Shows validation errors"
    ]
  },
  "files": {
    "src/components/Form.tsx": {
      "path": "src/components/Form.tsx",
      "content": "// Existing form component for reference...",
      "language": "typescript",
      "relevantSections": [
        { "startLine": 10, "endLine": 50, "description": "Form pattern" }
      ]
    }
  },
  "design": {
    "architecture": "React functional component with hooks",
    "patterns": ["controlled inputs", "form validation", "error display"]
  },
  "constraints": [
    "Follow existing Form component pattern",
    "Use project's validation library (zod)",
    "Match existing styling approach"
  ],
  "workingDirectory": "/path/to/project",
  "commitPrefix": "feat(auth)"
}
```

## Context Optimization

### File Selection

1. Include files directly mentioned in task
2. Include pattern files from same directory
3. Include type definitions if TypeScript
4. Limit to ~5 files maximum
5. Use relevant sections, not entire files

### Context Pruning

If context is too large:
1. Extract only relevant functions/classes
2. Remove comments and whitespace
3. Summarize repetitive patterns
4. Reference design.md instead of repeating

## Delegation Protocol

### Step 1: Prepare

```markdown
I am preparing to delegate Task {id} to a Codex worker.

**Task**: {title}
**Files to include**: {list}
**Constraints**: {list}
```

### Step 2: Delegate

```markdown
Delegating via MCP: mcp__codex__codex

Context package prepared with {n} files and {n} constraints.
```

Example payload:

```json
{
  "prompt": "TASK: Implement user login form\nEXPECTED OUTCOME: Working form with validation\nCONTEXT: {contextPackage JSON here}\nCONSTRAINTS: Follow existing patterns\nMUST DO: Update Login.tsx\nMUST NOT DO: Modify unrelated files\nOUTPUT FORMAT: Summary + files modified + signal"
}
```

### Step 3: Monitor

```markdown
Task {id} delegated to Codex worker.
Status: {pending|completed|failed}
```

### Step 4: Receive

```markdown
Received result from Codex worker.
Signal: {TASK_COMPLETE|TASK_BLOCKED|NO_SIGNAL}
Files modified: {count}
```

## Handling Worker Output

### On TASK_COMPLETE

1. Parse file modifications
2. Hand off to codex-reviewer
3. Wait for review decision

### On TASK_BLOCKED

1. Read block reason
2. Assess if CEO can unblock
3. If yes: Provide guidance and retry
4. If no: Escalate to user

### On NO_SIGNAL

1. Check if output looks complete
2. If yes: Treat as soft completion, verify carefully
3. If no: Retry with explicit signal instruction

## Retry Strategy

When retrying:

```json
{
  "previousAttempts": [
    {
      "attempt": 1,
      "feedback": "Missing validation on email field",
      "issues": [
        "Email input lacks validation",
        "Error messages not displayed"
      ]
    }
  ]
}
```

### Feedback Quality

Good feedback:
- "In Login.tsx line 23, add email regex validation"
- "The onSubmit handler doesn't prevent default"

Bad feedback:
- "Fix the validation"
- "It doesn't work"

## Token Efficiency

Track token usage:
```javascript
state.usage.codex.totalTokens += result.tokensUsed;
state.usage.codex.taskTokens[taskId] = result.tokensUsed;
```

Optimize by:
- Reusing context across related tasks
- Keeping prompts concise
- Extracting only necessary file content
