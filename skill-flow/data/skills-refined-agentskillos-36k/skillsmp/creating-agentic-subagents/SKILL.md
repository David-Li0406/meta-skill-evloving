---
name: creating-agentic-subagents
description: Create specialized agent configurations (subagents and primary agents) for OpenCode following research-backed best practices. Use when creating agents, configuring subagents, implementing multi-agent workflows, or when user mentions creating agents, subagents, agent configuration, specialized agents, multi-agent systems, or agent orchestration.
---

# Create Agentic Subagents

Create specialized agent configurations for OpenCode. Subagents are specialists invoked via @mention that operate in isolated context, while primary agents are main assistants users switch between with Tab.

## Core Principle: Start Simple

**Always begin with the simplest solution that could work.** Agentic systems trade latency and cost for capability. Only add complexity when simpler approaches fail.

```
Need to automate something?
├─ Can a single prompt with good context solve it?
│  └─ → Use main conversation (don't create an agent)
│
├─ Need reusable prompt with arguments?
│  └─ → Custom command (.opencode/command/)
│
├─ Need isolated context to prevent pollution?
│  └─ → Subagent with focused system prompt
│
├─ Need restricted tools for safety?
│  └─ → Subagent with tool/permission restrictions
│
├─ Need to switch between different modes?
│  └─ → Primary agent (mode: primary)
│
└─ Complex orchestration of specialists?
   └─ → Primary orchestrator + multiple subagents
```

## File Structure

**Project-specific:** `.opencode/agent/{name}.md`
**Global (all projects):** `~/.config/opencode/agent/{name}.md`

The filename becomes the agent identifier: `test-fixer.md` → `@test-fixer`

## Configuration Structure

```markdown
---
description: What the agent does and when to use it (REQUIRED)
mode: subagent # primary | subagent | all (default: all)
temperature: 0.1 # 0.0-1.0 (optional)
hidden: false # Hide from @autocomplete (optional, subagents only)
tools: # Tool restrictions (optional)
  write: false
  edit: false
  bash: false
disallowedTools: # Explicit tool denials (optional)
  - mcp__server__tool
skills: # Skills to load at startup (optional)
  - creating-feature-tests
hooks: # Lifecycle hooks (optional)
  PreToolUse:
    - matcher: 'Bash'
      hooks:
        - type: command
          command: './scripts/validate.sh'
permission: # Fine-grained permissions (optional)
  edit: deny
  bash:
    '*': ask
    'git status': allow
permissionMode: default # default | acceptEdits | dontAsk | plan (optional)
maxSteps: 50 # Limit agentic iterations (optional)
---

System prompt defining role, capabilities, and behavior.
```

### Required Fields

**`description`** - Critical for automatic delegation. Agents read this to decide when to invoke the subagent.

**Description formula:**

```
[What it does]. [Use proactively after X]. Use when [contexts] or when user mentions [keywords].
```

**Effective example:**

```yaml
description: Reviews code for quality, security, and best practices without making changes. Use proactively after code changes. Use for code review, quality checks, or when user mentions reviewing code or auditing quality.
```

Including "use proactively" encourages automatic delegation.

### Optional Fields

| Field             | Purpose                   | Values                                                              |
| ----------------- | ------------------------- | ------------------------------------------------------------------- |
| `mode`            | How agent can be used     | `primary`, `subagent`, `all`                                        |
| `temperature`     | Creativity vs determinism | 0.0-0.2 (analytical), 0.3-0.5 (balanced), 0.6-1.0 (creative)        |
| `hidden`          | Hide from @autocomplete   | `true`, `false`                                                     |
| `tools`           | Enable/disable tools      | `write`, `edit`, `bash`, `read`, `glob`, `grep`, `skill`, MCP tools |
| `disallowedTools` | Deny specific tools       | Array of tool names                                                 |
| `skills`          | Load skills at startup    | Array of skill names                                                |
| `hooks`           | Lifecycle callbacks       | `PreToolUse`, `PostToolUse`, `Stop`                                 |
| `permission`      | Fine-grained control      | `allow`, `ask`, `deny` per tool/command                             |
| `permissionMode`  | Permission behavior       | `default`, `acceptEdits`, `dontAsk`, `plan`                         |
| `maxSteps`        | Iteration limit           | Number (for cost control)                                           |

**Important:** Omit `model` unless user explicitly requests a specific model.

## Workflow Patterns

Design subagents around proven workflow patterns:

### Evaluator-Optimizer (Iterative)

Best for agents that iterate until success (test fixers, quality auditors):

```markdown
Workflow:

1. Run check/test
2. If passes → Report success and exit
3. Analyze failures
4. Fix issues
5. Repeat from step 1 until all pass

Exit criteria:

- All tests passing
- Coverage ≥90%
```

**Key elements:** Clear exit criteria, feedback loop with ground truth (test results).

### Read-Only Reviewer

Best for analysis without side effects (code review, security audit):

```yaml
tools:
  write: false
  edit: false
  bash: false
permission:
  edit: deny
```

**Key elements:** Cannot make changes, provides structured feedback.

### Orchestrator-Workers

Best for complex multi-step tasks delegated to specialists:

```yaml
permission:
  task:
    '*': deny
    'code-reviewer': allow
    'test-fixer': allow
```

**Key elements:** Delegates to specialists, synthesizes results.

See [references/patterns.md](references/patterns.md) for complete pattern templates.

## System Prompt Design

### Structure for Effective Prompts

1. **Role statement** (1-2 sentences)
2. **Focus areas** (what to examine/do)
3. **Workflow** (numbered steps with clear exit criteria)
4. **Guidelines** (what to do and avoid)
5. **Output format** (how to structure results)

### Key Principles

**Be specific about behavior:**

```markdown
# Good

Fix the root cause, not symptoms. Never remove failing tests to make them pass.

# Bad

Fix issues.
```

**Include ground truth feedback loops:**

```markdown
1. Run tests
2. Analyze results (ground truth)
3. Make changes
4. Re-run tests (verify against ground truth)
5. Repeat until passing
```

**Define clear exit criteria:**

```markdown
Exit when:

- All tests pass
- Coverage ≥90%
- No PHPStan errors

Final report format:
✅ All checks passing
✅ Coverage: X%
```

## Context and Cost Considerations

### The 15× Token Multiplier

Multi-agent systems use approximately **15× more tokens** than single conversations due to:

- Multiple isolated context windows
- Repeated tool calls across agents
- Parent-child communication overhead

### When Multi-Agent Is Worth It

**Use subagents when:**

- Context isolation genuinely helps (exploration won't pollute main conversation)
- Tool restrictions are needed for safety
- Task produces verbose output you don't need in main context
- Specialization produces measurably better results

**Stay single-agent when:**

- Task is simple or direct
- Sequential tasks share cumulative context
- Task value doesn't justify overhead

### Background vs Foreground

**Foreground subagents** (blocking):

- Permission prompts pass through to user
- Can ask clarifying questions
- Better for tasks needing human input

**Background subagents** (concurrent):

- Inherit parent permissions, auto-deny others
- Cannot ask questions (fail silently if needed)
- Better for parallel, independent tasks

## Quick Reference: Common Configurations

### Read-Only Reviewer

```yaml
temperature: 0.1
tools:
  write: false
  edit: false
  bash: false
permission:
  edit: deny
```

### Iterative Fixer (Full Access)

```yaml
temperature: 0.2
# No tool restrictions - needs to edit and run commands
```

### Path-Restricted Writer

```yaml
permission:
  bash: deny
  edit:
    'docs/*': allow
    'README.md': allow
    '*': deny
```

### Controlled Orchestrator

```yaml
permission:
  task:
    '*': deny
    'code-reviewer': allow
    'test-fixer': allow
```

## Anti-Patterns

**Creating too many agents:**
Over-specialization creates confusion. Most tasks need one `quality-auditor` or custom commands.

**Vague descriptions:**

```yaml
description: Helps with code review # ❌ No triggers, no context
```

**Missing exit criteria for iterative agents:**

```markdown
# ❌ No clear stopping point

Fix issues until done.

# ✅ Clear exit criteria

Repeat until all tests pass and coverage ≥90%.
```

**Skipping ground truth feedback:**

```markdown
# ❌ No verification

Make changes to fix the issue.

# ✅ Verified against ground truth

Make changes, run tests, verify fix worked.
```

## Quality Checklist

Before finalizing an agent:

- [ ] Clear `description` with purpose, triggers, and "use proactively" if appropriate
- [ ] Appropriate `mode` (primary vs subagent)
- [ ] Role and behavior clearly defined in system prompt
- [ ] Tool restrictions appropriate for agent purpose
- [ ] Permissions configured for safety
- [ ] Workflow has numbered steps (for iterative agents)
- [ ] Exit criteria explicitly defined
- [ ] Output format specified
- [ ] Ground truth feedback loop included (where applicable)
- [ ] `model` field omitted unless user specifically requested it
- [ ] Agent documented in AGENTS.md

## References

- [references/patterns.md](references/patterns.md) - Complete workflow patterns from Anthropic research
- [references/examples.md](references/examples.md) - Production-ready agent configurations
- [references/permissions.md](references/permissions.md) - Permission patterns, hooks, and context management
