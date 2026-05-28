# Claude Code Subagents: Complete Guide

## What Are Subagents?

Subagents are specialized AI assistants that Claude Code can delegate tasks to. Each subagent:
- Has a specific purpose and expertise area
- Uses its own context window separate from the main conversation
- Can be configured with specific tools it's allowed to use
- Includes a custom system prompt that guides its behavior

## Key Benefits

1. **Context Preservation** - Each subagent operates in its own context, preventing pollution of the main conversation
2. **Specialized Expertise** - Fine-tuned with detailed instructions for specific domains
3. **Reusability** - Can be used across different projects and shared with teams
4. **Flexible Permissions** - Each subagent can have different tool access levels

## Quick Start

```bash
/agents
```

This command opens an interactive interface where you can:
- View all available subagents
- Create new subagents with guided setup
- Edit existing custom subagents
- Delete custom subagents
- Manage tool permissions

## Subagent Configuration

### File Format

Subagents are stored as Markdown files with YAML frontmatter:

```yaml
---
name: your-sub-agent-name
description: Description of when this subagent should be invoked
tools: tool1, tool2, tool3  # Optional - inherits all tools if omitted
model: sonnet  # Optional - specify model alias or 'inherit'
permissionMode: default  # Optional - permission mode for the subagent
skills: skill1, skill2  # Optional - skills to auto-load
---

Your subagent's system prompt goes here...
```

### File Locations

| Type | Location | Scope | Priority |
|------|----------|-------|----------|
| **Project subagents** | `.claude/agents/` | Current project | Highest |
| **User subagents** | `~/.claude/agents/` | All projects | Lower |

### Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (lowercase + hyphens) |
| `description` | Yes | When/why to invoke this subagent |
| `tools` | No | Comma-separated tool list; omit to inherit all |
| `model` | No | Model alias (`sonnet`, `opus`, `haiku`) or `'inherit'` |
| `permissionMode` | No | `default`, `acceptEdits`, `bypassPermissions`, `plan`, `ignore` |
| `skills` | No | Comma-separated skill names to auto-load |

## CLI-Based Configuration

Define subagents dynamically using the `--agents` flag:

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

## Using Subagents Effectively

### Automatic Delegation

Claude Code proactively delegates tasks based on:
- The task description in your request
- The `description` field in subagent configurations
- Current context and available tools

To encourage proactive use, include phrases like "use PROACTIVELY" or "MUST BE USED" in your `description` field.

### Explicit Invocation

```bash
> Use the test-runner subagent to fix failing tests
> Have the code-reviewer subagent look at my recent changes
> Ask the debugger subagent to investigate this error
```

## Built-in Subagents

### 1. General-Purpose Subagent
- **Model**: Sonnet for complex reasoning
- **Tools**: All tools available
- **Purpose**: Complex research tasks, multi-step operations, code modifications
- **When used**: Tasks requiring both exploration and modification with complex reasoning

### 2. Plan Subagent
- **Model**: Sonnet for capable analysis
- **Tools**: Read, Glob, Grep, Bash
- **Purpose**: Researches codebase and gathers context before presenting plans
- **When used**: Automatically in plan mode when Claude needs to research codebase

### 3. Explore Subagent
- **Model**: Haiku for fast, low-latency searches
- **Mode**: Strictly read-only
- **Tools**: Glob, Grep, Read, Bash (read-only commands only)
- **Purpose**: Fast codebase searching and analysis
- **Thoroughness Levels**: Quick, Medium, Very thorough

## Example Subagents

### Code Reviewer

```yaml
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)
```

### Debugger

```yaml
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states
```

### Data Scientist

```yaml
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly
```

## Best Practices

✅ **Start with Claude-generated agents** - Generate initial subagents with Claude, then customize
✅ **Design focused subagents** - Single, clear responsibilities work best
✅ **Write detailed prompts** - Include specific instructions, examples, and constraints
✅ **Limit tool access** - Grant only necessary tools for the subagent's purpose
✅ **Version control** - Check project subagents into version control for team collaboration

## Advanced Usage

### Resumable Subagents

Continue previous agent conversations using the agent ID:

```bash
> Resume agent abc123 and now analyze the authorization logic
```

Each agent gets a unique `agentId` and transcript stored as `agent-{agentId}.jsonl`. This is useful for:
- Long-running codebase analysis
- Iterative refinement without losing context
- Multi-step workflows

### Chaining Subagents

```bash
> First use the code-analyzer subagent to find performance issues,
> then use the optimizer subagent to fix them
```

### Dynamic Subagent Selection

Claude Code intelligently selects subagents based on context. Make `description` fields specific and action-oriented for best results.

## Performance Considerations

- **Context Efficiency**: Subagents help preserve main context for longer sessions
- **Latency**: Subagents start fresh and may add latency as they gather required context
- **Read-only operations**: Explore subagent is optimized for fast searches without file modifications
