# Subagents and the Task Tool

> Create and use specialized AI subagents in Claude Code for task-specific workflows and improved context management.

## What Are Subagents?

Subagents are pre-configured AI personalities that Claude Code can delegate tasks to. They are specialized assistants that enable more efficient problem-solving by providing task-specific configurations with customized system prompts, tools, and a separate context window.

Each subagent:

- Has a specific purpose and expertise area
- Uses its own context window separate from the main conversation
- Can be configured with specific tools it is allowed to use
- Includes a custom system prompt that guides its behavior

When Claude Code encounters a task that matches a subagent's expertise, it can delegate that task to the specialized subagent, which works independently and returns results.

### Key Benefits

| Benefit | Description |
|---------|-------------|
| **Context Preservation** | Each subagent operates in its own context, preventing pollution of the main conversation and keeping it focused on high-level objectives |
| **Specialized Expertise** | Subagents can be fine-tuned with detailed instructions for specific domains, leading to higher success rates on designated tasks |
| **Reusability** | Once created, subagents can be used across different projects and shared with teams for consistent workflows |
| **Flexible Permissions** | Each subagent can have different tool access levels, allowing you to limit powerful tools to specific subagent types |

---

## The Task Tool

The Task tool is the internal mechanism Claude Code uses to spawn and manage subagents. When you invoke a subagent (either automatically or explicitly), Claude Code uses the Task tool behind the scenes.

### Task Tool Parameters

```typescript
interface TaskToolParams {
  description: string;      // Brief description of the task
  prompt: string;           // Detailed instructions for the subagent
  subagent_type?: string;   // Name of the subagent to use (optional)
  resume?: string;          // Agent ID to resume a previous session
}
```

### How Tasks Work

1. **Spawning**: When a task is created, a new subagent is spawned with its own context window
2. **Execution**: The subagent works independently using its configured tools
3. **Return**: Results are returned to the main conversation
4. **Recording**: Each execution gets a unique `agentId` for potential resumption

---

## Built-in Agent Types

Claude Code includes several built-in subagents available out of the box:

### 1. Explore Subagent

A fast, lightweight agent optimized for searching and analyzing codebases. Operates in strict read-only mode.

**Characteristics:**

- **Model**: Haiku (fast, low-latency)
- **Mode**: Strictly read-only - cannot create, modify, or delete files
- **Tools**: Glob, Grep, Read, Bash (read-only commands only: `ls`, `git status`, `git log`, `git diff`, `find`, `cat`, `head`, `tail`)

**When Used:**

Claude delegates to Explore when it needs to search or understand a codebase without making changes. This is more efficient than the main agent running multiple search commands directly.

**Thoroughness Levels:**

| Level | Description |
|-------|-------------|
| **Quick** | Fast searches with minimal exploration. Good for targeted lookups |
| **Medium** | Moderate exploration. Balances speed and thoroughness |
| **Very thorough** | Comprehensive analysis across multiple locations and naming conventions |

**Example:**

```
User: Where are errors from the client handled?

Claude: [Invokes Explore subagent with "medium" thoroughness]
[Explore uses Grep to search for error handling patterns]
[Explore uses Read to examine promising files]
[Returns findings with absolute file paths]
Claude: Client errors are handled in src/services/process.ts:712...
```

### 2. Plan Subagent

A specialized agent for use during plan mode. Used to conduct research and gather information about your codebase before presenting a plan.

**Characteristics:**

- **Model**: Sonnet (capable analysis)
- **Tools**: Read, Glob, Grep, Bash (for codebase exploration)
- **Purpose**: Search files, analyze code structure, gather context
- **Invocation**: Automatic when in plan mode

**How It Works:**

When you are in plan mode and Claude needs to understand your codebase to create a plan, it delegates research tasks to the Plan subagent. This prevents infinite nesting (subagents cannot spawn other subagents).

**Example:**

```
User: [In plan mode] Help me refactor the authentication module

Claude: Let me research your authentication implementation first...
[Internally invokes Plan subagent to explore auth-related files]
[Plan subagent searches codebase and returns findings]
Claude: Based on my research, here's my proposed plan...
```

### 3. General-Purpose Subagent

A capable agent for complex, multi-step tasks that require both exploration and action.

**Characteristics:**

- **Model**: Sonnet (capable reasoning)
- **Tools**: All tools available
- **Mode**: Can read and write files, execute commands, make changes
- **Purpose**: Complex research tasks, multi-step operations, code modifications

**When Used:**

- Task requires both exploration and modification
- Complex reasoning is needed to interpret search results
- Multiple strategies may be needed if initial searches fail
- Task has multiple steps that depend on each other

**Example:**

```
User: Find all the places where we handle authentication and update them to use the new token format

Claude: [Invokes general-purpose subagent]
[Agent searches for auth-related code across codebase]
[Agent reads and analyzes multiple files]
[Agent makes necessary edits]
[Returns detailed writeup of changes made]
```

---

## Custom Agent Creation

### Via /agents Command (Recommended)

```
/agents
```

This opens an interactive menu where you can:

- View all available subagents (built-in, user, and project)
- Create new subagents with guided setup
- Edit existing custom subagents, including their tool access
- Delete custom subagents
- See which subagents are active when duplicates exist
- Manage tool permissions

### Via File Creation

Subagents are stored as Markdown files with YAML frontmatter:

**File Locations:**

| Type | Location | Scope | Priority |
|------|----------|-------|----------|
| **Project subagents** | `.claude/agents/` | Available in current project | Highest |
| **User subagents** | `~/.claude/agents/` | Available across all projects | Lower |

When subagent names conflict, project-level subagents take precedence.

### File Format

```markdown
---
name: your-sub-agent-name
description: Description of when this subagent should be invoked
tools: tool1, tool2, tool3  # Optional - inherits all tools if omitted
model: sonnet  # Optional - specify model alias or 'inherit'
permissionMode: default  # Optional - permission mode for the subagent
skills: skill1, skill2  # Optional - skills to auto-load
---

Your subagent's system prompt goes here. This can be multiple paragraphs
and should clearly define the subagent's role, capabilities, and approach
to solving problems.

Include specific instructions, best practices, and any constraints
the subagent should follow.
```

### Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier using lowercase letters and hyphens |
| `description` | Yes | Natural language description of the subagent's purpose |
| `tools` | No | Comma-separated list of specific tools. If omitted, inherits all tools from the main thread |
| `model` | No | Model to use: `sonnet`, `opus`, `haiku`, or `inherit` |
| `permissionMode` | No | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan`, `ignore` |
| `skills` | No | Comma-separated list of skill names to auto-load (subagents do not inherit Skills from parent) |

### Via CLI Flag

Define subagents dynamically using the `--agents` CLI flag:

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

**Priority Order:** Project > CLI > User

---

## Model Selection

The `model` field controls which AI model the subagent uses:

| Value | Description |
|-------|-------------|
| `sonnet` | Default. Balanced capability and speed |
| `opus` | Most capable. Use for complex reasoning |
| `haiku` | Fastest. Use for simple, quick tasks |
| `inherit` | Use the same model as the main conversation |

**Note:** If `model` is omitted, defaults to `sonnet`.

Using `inherit` is useful when you want subagents to adapt to the model choice of the main conversation for consistency.

---

## Spawning Patterns

### Sequential Execution

Use sequential execution when tasks depend on each other:

```
> First use the code-analyzer subagent to find performance issues, then use the optimizer subagent to fix them
```

### Parallel Execution

Claude can invoke multiple subagents in parallel when tasks are independent. The main agent coordinates and combines results.

### Chaining Subagents

For complex workflows, chain multiple subagents:

```
> Use the test-runner to identify failing tests, then have the debugger subagent fix the root causes
```

**Important:** Subagents cannot spawn other subagents. This prevents infinite nesting.

### Background Agents

Subagents work independently and return results. The main conversation continues to manage high-level objectives while subagents handle specific tasks.

---

## Agent Resumption

Subagents can be resumed to continue previous conversations. Useful for long-running research or analysis tasks.

### How Resumption Works

1. Each subagent execution is assigned a unique `agentId`
2. The agent's conversation is stored in a transcript file: `agent-{agentId}.jsonl`
3. Resume by providing the `agentId` via the `resume` parameter
4. When resumed, the agent continues with full context from its previous conversation

### Example Workflow

**Initial invocation:**

```
> Use the code-analyzer agent to start reviewing the authentication module

[Agent completes initial analysis and returns agentId: "abc123"]
```

**Resume the agent:**

```
> Resume agent abc123 and now analyze the authorization logic as well

[Agent continues with full context from previous conversation]
```

### Use Cases for Resumption

- **Long-running research**: Break down large codebase analysis into multiple sessions
- **Iterative refinement**: Continue refining a subagent's work without losing context
- **Multi-step workflows**: Have a subagent work on related tasks sequentially while maintaining context

### Programmatic Resumption

```typescript
{
  "description": "Continue analysis",
  "prompt": "Now examine the error handling patterns",
  "subagent_type": "code-analyzer",
  "resume": "abc123"  // Agent ID from previous execution
}
```

---

## Best Practices

### 1. Start with Claude-Generated Agents

Generate your initial subagent with Claude, then iterate to customize. This gives you a solid foundation.

### 2. Design Focused Subagents

Create subagents with single, clear responsibilities rather than trying to make one subagent do everything.

**Good:**
- `code-reviewer` - Reviews code for quality and security
- `debugger` - Diagnoses and fixes bugs
- `test-runner` - Runs tests and reports failures

**Avoid:**
- `do-everything-agent` - Too broad, unpredictable behavior

### 3. Write Detailed Prompts

Include specific instructions, examples, and constraints:

```markdown
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations
```

### 4. Limit Tool Access

Only grant tools necessary for the subagent's purpose:

| Subagent Type | Recommended Tools |
|---------------|-------------------|
| Code reviewer | Read, Grep, Glob, Bash (read-only) |
| Debugger | Read, Edit, Bash, Grep, Glob |
| Test runner | Bash, Read, Glob |
| Data analyst | Bash, Read, Write |

### 5. Use Proactive Language in Descriptions

Include phrases like "use PROACTIVELY" or "MUST BE USED" to encourage automatic invocation:

```markdown
description: Expert code reviewer. MUST BE USED after ANY code changes.
```

### 6. Version Control Project Subagents

Check project subagents into version control (`.claude/agents/`) so your team benefits from and improves them.

---

## Common Patterns

### Code Reviewer Pattern

```markdown
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

Include specific examples of how to fix issues.
```

### Debugger Pattern

```markdown
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

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.
```

### Data Scientist Pattern

```markdown
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

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

Always ensure queries are efficient and cost-effective.
```

---

## Anti-Patterns

### 1. Overly Broad Subagents

**Avoid:** Creating a single subagent that handles everything.

```markdown
# Bad
name: general-helper
description: Helps with everything
```

**Why:** Reduces specialization benefits and makes behavior unpredictable.

### 2. Missing Description

**Avoid:** Vague or missing descriptions.

```markdown
# Bad
description: Does stuff
```

**Why:** Claude cannot intelligently decide when to use the subagent.

### 3. Granting All Tools Unnecessarily

**Avoid:** Giving every subagent access to all tools.

```markdown
# Bad - code reviewer doesn't need Edit
name: code-reviewer
tools: Read, Edit, Write, Bash, Grep, Glob, WebFetch, WebSearch
```

**Why:** Increases risk and reduces focus.

### 4. Expecting Subagent Nesting

**Avoid:** Designing workflows where subagents spawn other subagents.

```markdown
# Bad - subagents cannot spawn subagents
When you need more information, spawn the explore subagent...
```

**Why:** Subagents cannot spawn other subagents (prevents infinite nesting).

### 5. Ignoring Context Boundaries

**Avoid:** Assuming subagents share context with the main conversation.

**Why:** Each subagent has its own context window. Pass necessary information explicitly in the prompt.

---

## Performance Considerations

| Consideration | Impact |
|---------------|--------|
| **Context efficiency** | Subagents help preserve main context, enabling longer overall sessions |
| **Latency** | Subagents start fresh each time and may add latency as they gather context |
| **Model choice** | Use Haiku for fast, simple tasks; Sonnet for balanced work; Opus for complex reasoning |

---

## Plugin Agents

Plugins can provide custom subagents that integrate seamlessly with Claude Code.

**Plugin agent locations:** Plugins include agents in their `agents/` directory.

**Using plugin agents:**

- Appear in `/agents` alongside custom agents
- Can be invoked explicitly: "Use the code-reviewer agent from the security-plugin"
- Can be invoked automatically by Claude when appropriate
- Can be managed through the `/agents` interface

---

## Related Documentation

- [Skills](/en/skills) - Custom slash commands and workflows
- [Hooks](/en/hooks) - Automate workflows with event handlers
- [Settings](/en/settings) - Configure Claude Code behavior
- [Tools](/en/settings#tools-available-to-claude) - Available tools reference
