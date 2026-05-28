# Permission Modes: Control and Safety

Understanding permission modes for secure and flexible subagent management.

## Permission Mode Options

Each mode controls how agents handle permission requests during execution.

### 1. default (Safest)

**Behavior**: Agent asks for approval on sensitive operations

**What requires permission**:
- Creating files
- Modifying files
- Deleting files
- Executing bash commands
- Making web requests

**User experience**:
- Agent pauses execution
- Shows pending operation
- User chooses: Approve / Deny
- Execution continues based on user choice

**When to use**:
- Untrusted or external workflows
- Sensitive operations on important codebase
- Learning/testing agent behavior
- First-time agent deployments
- Any agent you're unsure about

**Example**:
```yaml
---
name: code-reviewer
description: Analyzes code for quality issues and security concerns
permissionMode: default
---
```

**Agent interaction**:
```
Agent: "I want to create a report file: analysis.md. Approve? (Y/n)"
User: "Y"
[Agent creates file and continues]
```

---

### 2. acceptEdits (Trusted Refactoring)

**Behavior**: Agent auto-accepts file edit operations; still asks for other permissions

**Operations auto-approved**:
- Reading files
- Writing files
- Editing files
- Creating files

**Operations still requiring approval**:
- Deleting files
- Bash command execution
- Web requests

**When to use**:
- Code refactoring agents (safe to modify files)
- Trusted code generation workflows
- Automated testing/fixing agents
- Agents that improve existing code

**Example**:
```yaml
---
name: code-formatter
description: Automatically formats Python code for readability and PEP 8 compliance
permissionMode: acceptEdits
---
```

**Agent interaction**:
```
Agent: "I'll format src/main.py for PEP 8 compliance..."
[Agent automatically edits file without asking]
Agent: "I want to run: python -m black src/ . Approve? (Y/n)"
User: "Y"
[Bash command requires approval]
```

**Trade-off**: Enables faster workflows for trusted operations while maintaining safety for destructive operations.

---

### 3. bypassPermissions (Fully Trusted)

**Behavior**: Agent bypasses ALL permission checks

**Operations executed without approval**:
- Creating, reading, modifying, deleting files
- Bash command execution
- Web requests
- All other operations

**When to use**:
- Fully trusted, repeated workflows
- Production automation
- Team-standardized agents in controlled environments
- Agents with strict tool restrictions (enforcing safety via tools rather than permissions)

**When NOT to use**:
- Experimental agents
- External/community agents
- Sensitive data environments
- Learning/testing scenarios

**Example**:
```yaml
---
name: ci-automation-trusted
description: Automated CI/CD pipeline operations for trusted repository
tools: Read, Write, Bash, Grep
permissionMode: bypassPermissions
---
```

**Risk considerations**:
- Agent can modify/delete any files
- Agent can execute any bash commands
- Use `tools` field to restrict dangerous operations
- Consider combining with tool restrictions for safety

**Safety pattern**: Restrict tools first, then use bypassPermissions
```yaml
---
name: safe-ci-agent
description: Automated build and test operations
tools: Read, Bash, Grep  # No Write/Edit - read-only for safety
permissionMode: bypassPermissions
---
```

---

### 4. plan (Planning Context)

**Behavior**: Agent automatically switches to plan mode

**Characteristics**:
- Agent operates in non-execution context
- Returns plan without implementing
- User can review before execution
- No file modifications or commands execute
- Focuses on strategy and design

**When to use**:
- Planning/architectural agents
- Design review agents
- Strategy recommendation agents
- Any agent that should output plan without execution

**Example**:
```yaml
---
name: refactoring-planner
description: Plans code refactoring strategies without executing changes
permissionMode: plan
---
```

**Agent behavior**:
```
Agent: "Here's my refactoring plan:
1. Extract authentication logic to separate module
2. Create interface abstraction
3. Update 12 files with new imports
4. Run tests to validate

Ready to execute? (User must explicitly ask for execution)"
```

**Advantage**: Complete review cycle before any changes applied

---

### 5. ignore (Special Operations)

**Behavior**: Agent ignores specific permission checks

**Use case**: When certain operations shouldn't trigger permission dialogs
- Agent continues without interruption
- Useful for high-frequency operations

**When to use**:
- Agents that repeatedly perform similar safe operations
- Reducing permission dialog fatigue
- Operations determined safe by design

**Example**:
```yaml
---
name: log-analyzer
description: Analyzes application logs for error patterns
permissionMode: ignore
---
```

**Comparison with bypassPermissions**:
- `ignore`: Ignores specific permission checks (selective)
- `bypassPermissions`: Bypasses all permission checks (global)

**Note**: Practical difference minimal - choose `default` or `bypassPermissions` based on trust level.

---

## Decision Framework: Which Mode?

### Ask These Questions

**Q1: How much do I trust this agent?**
- Not yet tested → `default`
- Proven reliable → `acceptEdits` or `bypassPermissions`
- Production approved → `bypassPermissions`

**Q2: What operations will the agent perform?**
- Only analysis/reading → any mode works
- File modifications (refactoring, formatting) → `acceptEdits` or higher
- Deletions, command execution → `bypassPermissions` or tool restrictions
- Planning only → `plan`

**Q3: What's the risk if something goes wrong?**
- High risk (production code, critical data) → `default` or `acceptEdits`
- Medium risk (development, experimental) → `acceptEdits`
- Low risk (isolated, reversible) → `bypassPermissions` safe

**Q4: How often will this agent run?**
- One-time → `default` (safety first)
- Repeated/automated → `bypassPermissions` (efficiency)
- Interactive/manual → `default` (user control)

---

## Mode Selection Matrix

| Agent Type | Trust Level | Operations | Recommended Mode |
|------------|------------|------------|-----------------|
| New agent | Low | Unknown | `default` |
| Code formatter | High | Write/Edit | `acceptEdits` |
| Code reviewer | Medium | Read/Analyze | `default` |
| CI automation | Very High | Write/Bash | `bypassPermissions` |
| Refactoring planner | Medium | None (plan only) | `plan` |
| Security auditor | Medium | Read/Analyze | `default` |
| Test runner | High | Bash/Write | `acceptEdits` |
| Data processor | High | Write/Read | `acceptEdits` |

---

## Implementation Examples

### Example 1: Safe Testing Agent
```yaml
---
name: test-runner
description: Runs test suite, identifies failures, provides diagnostics
tools: Read, Bash, Grep
permissionMode: default  # Approve bash execution
---

Run tests and report failures...
```

### Example 2: Trusted Formatter
```yaml
---
name: code-formatter
description: Formats code to project standards
permissionMode: acceptEdits  # Auto-approve edits, safe operations
---

Format files to project standards...
```

### Example 3: Production Automation
```yaml
---
name: deployment-bot
description: Automates deployment pipeline operations
tools: Read, Bash, Grep  # No destructive tools
permissionMode: bypassPermissions  # Trusted, restricted tools
---

Execute deployment commands...
```

### Example 4: Strategy Agent
```yaml
---
name: architecture-planner
description: Proposes system architecture improvements
permissionMode: plan  # Always plan mode
---

Design improved architecture...
```

---

## Best Practices

1. **Start with default**: Conservative default for unknown agents
2. **Escalate gradually**: Move to higher permissions as trust builds
3. **Combine with tools**: Restrict dangerous tools + use permission mode for additional safety
4. **Document rationale**: Note why you chose each mode in agent config comments
5. **Review periodically**: Audit permission modes for agents you've created
6. **Never use bypassPermissions for experimental agents**: Too risky
7. **Use plan mode for architectural agents**: Ensures review before implementation

