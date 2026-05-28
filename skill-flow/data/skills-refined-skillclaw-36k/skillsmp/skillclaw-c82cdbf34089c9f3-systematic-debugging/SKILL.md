---
name: systematic-debugging
description: Use this skill when you need to systematically debug issues, analyze errors, or troubleshoot incidents in your code or system.
---

# Skill body

## Trigger Conditions

- Debugging code issues
- Analyzing error logs
- Investigating performance problems
- Troubleshooting production incidents
- Fixing bugs

## Debugging Principles

### Golden Rules

1. **Reproduce the Issue** - Ensure you can consistently reproduce the problem before starting the debugging process.
2. **Minimize** - Identify the smallest possible case that reproduces the issue.
3. **Binary Search** - Narrow down the scope of the problem.
4. **Hypothesis Testing** - Formulate hypotheses and validate them.
5. **Document the Process** - Keep a record of the methods you have tried.

### Debugging Process

```
Problem Description → Reproduce Issue → Narrow Down → Identify Cause → Fix and Validate → Document Summary
```

## Problem Description Template

```markdown
## Problem Description

[Briefly describe the observed issue]

## Expected Behavior

[What the correct behavior should be]

## Actual Behavior

[What behavior was actually observed]

## Steps to Reproduce

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Environment Information

- OS: [Operating System]
- Node/Python Version: [Version]
- Relevant Dependency Versions: [Version]

## Error Information

[Complete error stack or logs]

## Attempts Made

- [ ] Attempt 1 - Result
- [ ] Attempt 2 - Result
```

## Effective Logging

### Example of Useful Logs

```typescript
// ❌ Useless log
console.log("here");
console.log(data);

// ✅ Informative log
console.log("[UserService.createUser] Starting user creation:", {
  email: user.email,
  timestamp: new Date().toISOString(),
});

console.log("[UserService.createUser] Database insert successful:", {
  userId: result.id,
  duration: Date.now() - startTime,
});

console.error("[UserService.createUser] Creation failed:", {
  error: error.message,
  stack: error.stack,
  input: { email: user.email },
});
```

```python
# ❌ Useless log
print("here")
print(data)

# ✅ Informative log
import logging
logger = logging.getLogger(__name__)

logger.info(f"[create_user] Starting user creation: email={email}")
logger.info(f"[create_user] Creation successful: user_id={user.id}, duration={duration}ms")
logger.error(f"[create_user] Creation failed: error={str(e)}", exc_info=True)
```

### Log Level Usage

| Level  | Purpose           | Example               |
| ------ | ----------------- | --------------------- |
| DEBUG  | Detailed debug info| Function parameters, intermediate states |
| INFO   | Normal operation info| User logins, order creations |
| WARN   | Warning but can continue| Missing configuration defaults to use |
| ERROR  | Recoverable error  | API call failure retry |
| FATAL  | Critical error requiring exit| Database connection failure |
  
## Breakpoint Debugging

### VS Code Debug Configuration

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Node.js",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/src/index.ts",
      "preLaunchTask": "tsc: build",
      "outFiles": ["${workspaceFolder}/dist/**/*.js"]
    },
    {
      "name": "Debug Python",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    },
    {
      "name": "Debug Jest Tests",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/.bin/jest",
      "args": ["--runInBand"],
```