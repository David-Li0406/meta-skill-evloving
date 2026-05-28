# Permissions, Hooks, and Context Management

Fine-grained control over agent capabilities, lifecycle events, and context optimization.

## Permission Patterns

### Pattern 1: Tool Allowlisting

Enable only specific tools:

```yaml
tools:
  read: true
  glob: true
  grep: true
  write: false
  edit: false
  bash: false
```

### Pattern 2: Tool Denylisting

Inherit all tools except specific ones:

```yaml
disallowedTools:
  - mcp__puppeteer__puppeteer_navigate
  - mcp__database__execute_query
```

### Pattern 3: Bash Command Restrictions

Allow specific safe commands, ask for others:

```yaml
permission:
  bash:
    '*': ask # Ask for all by default
    'git status': allow # Always allow git status
    'git log*': allow # Allow all git log variations
    'git diff*': allow # Allow all git diff
    'npm test': allow # Allow running tests
    'composer test': allow
    'rm *': deny # Never allow rm
    'git reset --hard*': deny
```

**Note:** Rules are evaluated in order, **last matching rule wins**. Place `*` wildcards first.

### Pattern 4: Complete Lockdown

Read-only agent for pure analysis:

```yaml
tools:
  write: false
  edit: false
  bash: false
permission:
  edit: deny
  bash: deny
  webfetch: deny
```

### Pattern 5: Path-Specific Write Access

Restrict edits to specific directories:

```yaml
permission:
  edit:
    'docs/*': allow # Allow docs directory
    'README.md': allow # Allow README
    '*.md': ask # Ask for other markdown
    '*': deny # Deny everything else
```

### Pattern 6: Task Orchestration Control

Control which subagents can be invoked:

```yaml
permission:
  task:
    '*': deny # Deny all by default
    'code-reviewer': allow # Allow code reviewer
    'test-fixer': allow # Allow test fixer
    'security-auditor': ask # Ask before security audit
```

### Permission Modes

Set overall permission behavior with `permissionMode`:

| Mode                | Behavior                                      |
| ------------------- | --------------------------------------------- |
| `default`           | Standard permission checking with prompts     |
| `acceptEdits`       | Auto-accept file edits                        |
| `dontAsk`           | Auto-deny permission prompts                  |
| `bypassPermissions` | Skip all permission checks (use with caution) |
| `plan`              | Plan mode (read-only exploration)             |

```yaml
permissionMode: acceptEdits # Auto-accept edits
```

**Warning:** `bypassPermissions` is dangerous. If parent uses it, subagent inherits it and cannot override.

## Lifecycle Hooks

Hooks run code at specific points in the agent lifecycle.

### Hook Types

| Event         | Matcher   | When it fires       |
| ------------- | --------- | ------------------- |
| `PreToolUse`  | Tool name | Before using a tool |
| `PostToolUse` | Tool name | After using a tool  |
| `Stop`        | (none)    | When agent finishes |

### Hooks in Subagent Frontmatter

Define hooks that run only while the subagent is active:

```yaml
hooks:
  PreToolUse:
    - matcher: 'Bash'
      hooks:
        - type: command
          command: './scripts/validate-command.sh $TOOL_INPUT'
  PostToolUse:
    - matcher: 'Edit|Write'
      hooks:
        - type: command
          command: './scripts/run-linter.sh'
  Stop:
    - hooks:
        - type: command
          command: './scripts/cleanup.sh'
```

### Use Cases for Hooks

**Command validation:**

```yaml
hooks:
  PreToolUse:
    - matcher: 'Bash'
      hooks:
        - type: command
          command: './scripts/validate-readonly-query.sh'
```

The script inspects `$TOOL_INPUT` and exits non-zero to block the command.

**Post-edit linting:**

```yaml
hooks:
  PostToolUse:
    - matcher: 'Edit'
      hooks:
        - type: command
          command: 'composer pint --dirty'
```

**Debug logging:**

```yaml
hooks:
  PreToolUse:
    - matcher: 'Bash'
      hooks:
        - type: command
          command: "echo 'Running: $TOOL_INPUT' >> /tmp/agent-debug.log"
```

## Context Management

### How Context Flows

**Parent → Subagent:**

- Task description via Task tool invocation
- Subagent receives prompt but NOT parent's conversation history
- Fresh, isolated context for each invocation

**Subagent → Parent:**

- Condensed findings returned through Task tool result
- Subagents act as intelligent filters
- Return conclusions, not raw search results

**Between Invocations:**

- Subagents have NO memory between invocations
- Each spawn starts fresh with clean context
- Parent maintains conversation history

### Context Isolation Benefits

1. **Prevents pollution**: Exploration doesn't clutter main conversation
2. **Enables longer sessions**: Parent context doesn't fill with intermediate work
3. **Focuses attention**: Each subagent has clean context for its task
4. **Compresses information**: Only relevant findings returned to parent

### Background vs Foreground Execution

**Foreground subagents** (blocking):

- Block main conversation until complete
- Permission prompts pass through to user
- Can ask clarifying questions via `AskUserQuestion`
- Better for tasks needing human input

**Background subagents** (concurrent):

- Run while user continues working
- Inherit parent permissions, auto-deny others
- If needs permission or question, that call fails (agent continues)
- MCP tools not available in background
- Better for parallel, independent tasks

To background a running task, press **Ctrl+B**.

### Resuming Subagents

Subagent invocations create new instances with fresh context. To continue previous work:

```
Use the code-reviewer subagent to review authentication.
[Agent completes]

Continue that review and now analyze authorization.
[Claude resumes with full context from previous]
```

Resumed subagents retain full conversation history.

### Auto-Compaction

When context approaches limit, older messages are summarized automatically:

- Preserves important context
- Frees space for new work
- Logged in subagent transcripts

## Cost Considerations

### The 15× Token Multiplier

Multi-agent systems use approximately **15× more tokens** than single conversations:

- Multiple isolated context windows
- Repeated tool calls across agents
- Parent-child communication overhead
- Model running multiple times

### When the Cost Is Worth It

**Use multi-agent when:**

- Tasks genuinely benefit from parallelization
- Context would overflow single agent
- Specialization produces measurably better results
- High-value outcomes justify increased cost
- Need isolated contexts to prevent pollution

**Stay single-agent when:**

- Simple fact-finding or direct queries
- Sequential tasks with cumulative context
- Task value doesn't justify 15× overhead
- No genuine need for specialization

### Cost Optimization Strategies

1. **Route simple tasks to lighter models** (if user requests)
2. **Compress subagent outputs** in system prompt:
   ```markdown
   Return compressed findings:

   - File references with brief descriptions
   - Key patterns identified
   - Recommendations (not raw data)
   ```
3. **Limit subagent invocations** to necessary tasks only
4. **Clear, focused task descriptions** reduce wasted iterations
5. **Appropriate tool restrictions** prevent unnecessary work
6. **Use maxSteps** to limit iterations:
   ```yaml
   maxSteps: 20 # Force summary after 20 steps
   ```

## Skills Integration

Load skills into subagent context at startup:

```yaml
skills:
  - creating-actions
  - creating-dtos
  - writing-feature-tests
```

**Important:** Skills are fully loaded at startup, not invoked on-demand. The entire skill content is injected into context.

### When to Use Skills with Subagents

- Agent needs domain-specific patterns
- Multiple skills provide comprehensive workflow
- Skills are smaller than embedding in system prompt
- Same skills used across multiple agents

### Skills vs System Prompt

| Approach      | When to Use                                      |
| ------------- | ------------------------------------------------ |
| System prompt | Agent-specific behavior, workflow, output format |
| Skills        | Reusable domain knowledge, shared patterns       |

Example combining both:

```yaml
---
description: Builds features following domain patterns
skills:
  - creating-actions
  - creating-dtos
---
You are a feature builder.

[Agent-specific workflow here]

Follow patterns from your loaded skills for Actions and DTOs.
```

## Disabling Agents

### Disable via Settings

Add to permissions deny list:

```json
{
  "permissions": {
    "deny": ["Task(Explore)", "Task(my-custom-agent)"]
  }
}
```

### Disable via CLI

```bash
claude --disallowedTools "Task(Explore)"
```

### Hidden Agents

Hide from @autocomplete but allow programmatic invocation:

```yaml
hidden: true
```

Only applies to `mode: subagent` agents.
