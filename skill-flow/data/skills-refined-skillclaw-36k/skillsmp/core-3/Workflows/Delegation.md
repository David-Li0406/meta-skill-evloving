# Delegation Workflow

Comprehensive guide to delegating tasks to agents in PAI.

## Agent Type Selection

**Determine what the user is asking for:**

| User Says | Action | Tool |
|-----------|--------|------|
| "spin up agents", "launch agents", "bunch of agents" | Use **general-purpose** agents for parallel work | `Task(subagent_type="general-purpose")` |
| "explore the codebase", "find files" | Use **Explore** agent | `Task(subagent_type="Explore")` |
| "plan this out", "design the approach" | Use **Plan** agent | `Task(subagent_type="Plan")` |

---

## How the User Interacts

**Users just talk naturally.** Examples:

- "Research these 5 companies for me" → I spawn 5 parallel general-purpose agents
- "Explore the codebase for auth patterns" → I use Explore agent
- "Plan out the architecture for this feature" → I use Plan agent

**Users never touch CLI tools.** The system uses them internally based on what you ask for.

## Triggers

- "delegate", "spawn agents", "launch agents" → general-purpose
- "explore codebase", "find files" → Explore
- "plan this", "design approach" → Plan
- "in parallel", "parallelize" → Multiple general-purpose agents

## Available Subagent Types

| Subagent Type | Purpose | When Used |
|---------------|---------|-----------|
| `general-purpose` | Multi-step tasks, research, analysis | Default for parallel work |
| `Explore` | Codebase exploration | Finding files, understanding structure |
| `Plan` | Implementation planning | Architecture design, plan mode |
| `Bash` | Command execution | Running shell commands |
| `claude-code-guide` | Claude Code help | Questions about Claude Code features |

## Model Selection

**CRITICAL FOR SPEED**: Always specify the right model for the task.

| Task Type | Model | Why |
|-----------|-------|-----|
| Deep reasoning, architecture | `opus` | Maximum intelligence |
| Standard implementation, analysis | `sonnet` | Balance of speed + capability |
| Simple checks, parallel grunt work | `haiku` | 10-20x faster, sufficient |

```typescript
// WRONG - defaults to Opus, takes minutes
Task({ prompt: "Check if file exists", subagent_type: "general-purpose" })

// RIGHT - Haiku for simple task
Task({ prompt: "Check if file exists", subagent_type: "general-purpose", model: "haiku" })
```

**Rule of Thumb:**
- Grunt work or verification → `haiku`
- Implementation or research → `sonnet`
- Strategic/architectural → `opus` or default

## Foreground Delegation

Standard blocking delegation - waits for agent to complete.

### Single Agent

```typescript
Task({
  description: "Research competitor",
  prompt: "Investigate Acme Corp's recent product launches...",
  subagent_type: "general-purpose",
  model: "sonnet"
})
// Blocks until complete, returns result
```

### Parallel Agents

**ALWAYS use a single message with multiple Task calls for parallel work:**

```typescript
// Send as SINGLE message with multiple tool calls
Task({
  description: "Research company A",
  prompt: "Investigate Company A...",
  subagent_type: "general-purpose",
  model: "haiku"
})
Task({
  description: "Research company B",
  prompt: "Investigate Company B...",
  subagent_type: "general-purpose",
  model: "haiku"
})
Task({
  description: "Research company C",
  prompt: "Investigate Company C...",
  subagent_type: "general-purpose",
  model: "haiku"
})
// All run in parallel, all results returned together
```

### Spotcheck Pattern

**ALWAYS launch a spotcheck agent after parallel work:**

```typescript
// After parallel agents complete
Task({
  description: "Spotcheck parallel results",
  prompt: "Review these results for consistency and completeness: [results]",
  subagent_type: "general-purpose",
  model: "haiku"
})
```

## Background Delegation

Non-blocking delegation - agents run while you continue working.

See: `Workflows/BackgroundDelegation.md` for full details.

```typescript
Task({
  description: "Background research",
  prompt: "Research X...",
  subagent_type: "general-purpose",
  model: "haiku",
  run_in_background: true  // Returns immediately
})
// Returns { agent_id: "abc123", status: "running" }

// Check later
TaskOutput({ agentId: "abc123", block: false })

// Retrieve when ready
TaskOutput({ agentId: "abc123", block: true })
```

## Decision Matrix

### Foreground vs Background

| Situation | Choice | Reason |
|-----------|--------|--------|
| Need results immediately | Foreground | Blocking is fine |
| Have other work to do | Background | Don't want to wait |
| 3+ parallel tasks | Background | More flexible |
| Single quick task | Foreground | Simpler |

## Full Context Requirements

When delegating, ALWAYS include:

1. **WHY** - Business context, why this matters
2. **WHAT** - Current state, existing implementation
3. **EXACTLY** - Precise actions, file paths, patterns
4. **SUCCESS CRITERIA** - What good output looks like

```typescript
Task({
  description: "Audit auth security",
  prompt: `
    ## Context
    We're preparing for SOC 2 audit. Need to verify our auth implementation.

    ## Current State
    Auth is in src/auth/, uses JWT with refresh tokens.

    ## Task
    1. Review all auth-related code
    2. Check for OWASP Top 10 vulnerabilities
    3. Verify token handling is secure
    4. Check for timing attacks in password comparison

    ## Success Criteria
    - Comprehensive security assessment
    - Specific file:line references for any issues
    - Severity ratings for each finding
    - Remediation recommendations
  `,
  subagent_type: "general-purpose",
  model: "sonnet"
})
```

## Related

- Background delegation: `~/.claude/skills/CORE/Workflows/BackgroundDelegation.md`
- Agent system reference: `~/.claude/skills/CORE/SYSTEM/PAIAGENTSYSTEM.md`
