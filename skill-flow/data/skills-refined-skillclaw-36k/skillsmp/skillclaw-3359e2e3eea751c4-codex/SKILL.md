---
name: codex
description: Use this skill when you need to execute code changes, including writing, modifying, and deleting code, as well as managing testing and file operations.
---

# Codex Skill

Codex is the primary method for executing code changes. Claude is responsible for planning and validation, while Codex handles the actual execution.

## Core Principles

> **"First, solve the problem. Then, write the code."** — John Johnson

Follow the KISS principle: write the least amount of code to solve the problem.

## Use Cases

- Any code writing, modification, or deletion
- Writing and executing tests (upon user request)
- Large-scale refactoring
- File operations

## Invocation Methods

### Basic Invocation
```bash
codex "task description" [working directory]
codex "refactor @src/auth.ts add JWT validation"
```

### HEREDOC Syntax (Recommended for Complex Tasks)
```bash
codex - <<'EOF'
Implement user authentication module:
1. Create login API endpoint
2. Add JWT token generation
3. Implement password hashing
4. Write unit tests (only upon user request)
EOF
```

### Parallel Execution
```bash
codex --parallel <<'EOF'
---TASK---
id: backend_api
workdir: /project/backend
---CONTENT---
Implement /api/users endpoint

---TASK---
id: frontend_ui
workdir: /project/frontend
dependencies: backend_api
---CONTENT---
Create Users page
EOF
```

## Session Management

```bash
# First task
codex "add form validation"
# Output: SESSION_ID: 019a7247...

# Resume session
codex resume 019a7247... - <<'EOF'
Add error messages for each validation rule
EOF
```

## Self-Repair Loop

```
Execute → Fail? → Analyze → Fix → Retry (max 3)
                                    ↓
                           Halt: Request human intervention
```

## Code Quality Standards

### Must-Haves
- TypeScript without `any`
- Complete error handling
- Input validation

### Avoid
- Over-abstraction
- Defensive over-design
- Magic numbers/hardcoding

## Degradation Strategy

1. Codex is the preferred execution method.
2. Retry once on failure.
3. After two consecutive failures, log CODEX_FALLBACK and let Claude execute directly.
4. Retry Codex on the next task.

## Note

**Default silent execution**: Unless explicitly requested by the user, do not automatically run tests/compilation.