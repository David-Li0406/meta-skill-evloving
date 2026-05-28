---
name: codex
description: Use this skill for executing and managing code changes, including writing, modifying, and testing code.
---

# Codex Skill

The primary method for code execution. Claude handles planning and validation, while Codex executes the actual code.

## Core Principles

> **"First, solve the problem. Then, write the code."** — John Johnson

Follow the KISS principle: write the least amount of code to solve the problem.

## Use Cases

- Any code writing, modification, or deletion
- Test writing and execution (upon user request)
- Large-scale refactoring
- File operations

## Invocation Methods

### Basic Invocation
```bash
codex "task description" [working directory]
codex "refactor @src/auth.ts add JWT validation"
```

### HEREDOC Syntax (recommended for complex tasks)
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

### Session Management
```bash
# First task
codex "add form validation"
# Output: SESSION_ID: 019a7247...

# Resume session
codex resume 019a7247... - <<'EOF'
Add error messages for each validation rule
EOF
```

## Self-Check Before Execution (Linus Review)

```markdown
- [ ] Is the data structure the simplest possible?
- [ ] Are there unnecessary abstractions?
- [ ] Do names accurately reflect their essence?
- [ ] Functions <50 lines, components <200 lines?
- [ ] Is there complete error handling?
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
3. After two consecutive failures → log CODEX_FALLBACK → Claude executes directly.
4. Retry Codex for the next task.

## Note

**Default silent execution**: Tests/compilation do not run automatically unless explicitly requested by the user.